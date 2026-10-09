import struct

SEARCH_SIZE, LOOKAHEAD_SIZE = 4096, 32
HEADER = b"LZ77PY01"
MIN_MATCH = 3
OUTPUT_BUFFER_SIZE = 8192


def write_header(dest, search, lookahead):
    dest.write(HEADER + struct.pack(">HH", search, lookahead))


def read_header(src):
    if src.read(len(HEADER)) != HEADER:
        raise ValueError("Invalid file")
    return struct.unpack(">HH", src.read(4))


def find_match(window, data, lkah_size):
    best_offset, best_length = 0, 0
    limit = min(len(data), lkah_size)

    for pos in range(len(window) - 1, -1, -1):
        offset, length = len(window) - pos, 0

        while length < limit:
            expected = (window[pos + length] if length < offset
                        else data[length - offset])
            if expected != data[length]:
                break
            length += 1

        if length > best_length:
            best_offset, best_length = offset, length
            if length == limit:
                break

    return best_offset, best_length


def compress_file(input_path, output_path, search=SEARCH_SIZE,
                  lookahead=LOOKAHEAD_SIZE):
    window, data = bytearray(), bytearray()

    with open(input_path, "rb") as src, open(output_path, "wb") as dest:
        write_header(dest, search, lookahead)
        data.extend(src.read(lookahead))

        while data:
            offset, length = find_match(window, data, lookahead)

            if length >= MIN_MATCH:
                dest.write(struct.pack(">BHH", 1, offset, length))
                consumed = length
            else:
                dest.write(struct.pack(">BB", 0, data[0]))
                consumed = 1

            window.extend(data[:consumed])
            del window[:-search]
            del data[:consumed]
            data.extend(src.read(lookahead - len(data)))

    print(f"Compressed: {input_path} -> {output_path}")


def decompress_file(input_path, output_path):
    window, buffer = bytearray(), bytearray()

    with open(input_path, "rb") as src, open(output_path, "wb") as dest:
        search, lookahead = read_header(src)

        def emit(byte):
            buffer.append(byte)
            if len(buffer) >= OUTPUT_BUFFER_SIZE:
                dest.write(buffer)
                buffer.clear()

        while flag := src.read(1):
            if flag[0] == 0:
                byte = src.read(1)[0]
                emit(byte)
                window.append(byte)
            else:
                offset, length = struct.unpack(">HH", src.read(4))
                for _ in range(length):
                    byte = window[-offset]
                    emit(byte)
                    window.append(byte)

            if len(window) > search:
                del window[:-search]

        if buffer:
            dest.write(buffer)

    print(f"Decompressed: {input_path} -> {output_path}")



def main():
    command = input("Compress or decompress? (c/d): ").lower()
    input_path = input("Input file path: ")
    output_path = input("Output file path: ")

    print("Input path:", repr(input_path))

    if command == "c":
        compress_file(input_path, output_path, SEARCH_SIZE, LOOKAHEAD_SIZE)
    elif command == "d":
        decompress_file(input_path, output_path)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
