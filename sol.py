from dataclasses import dataclass
from typing import Optional


@dataclass
class Token:
    offset: int
    length: int
    next_char: Optional[str]
    has_next_char: bool


def compress_lz77(s: str) -> list[Token]:
    result: list[Token] = []
    pos = 0
    n = len(s)

    while pos < n:
        best_offset = 0
        best_length = 0

        for start in range(pos - 1, -1, -1):
            length = 0

            while (
                pos + length < n
                and start + length < n
                and s[start + length] == s[pos + length]
            ):
                length += 1

            if length > best_length:
                best_length = length
                best_offset = pos - start

        next_pos = pos + best_length

        if next_pos < n:
            result.append(Token(best_offset, best_length, s[next_pos], True))
            pos = next_pos + 1
        else:
            result.append(Token(best_offset, best_length, None, False))
            pos = next_pos

    return result


def decompress_lz77(tokens: list[Token]) -> str:
    out: list[str] = []

    for t in tokens:
        for _ in range(t.length):
            out.append(out[len(out) - t.offset])

        if t.has_next_char and t.next_char is not None:
            out.append(t.next_char)

    return "".join(out)


if __name__ == "__main__":
    user_input = input("Enter the string: ")

    compressed = compress_lz77(user_input)

    print("Compressed tokens:")
    for t in compressed:
        if t.has_next_char:
            print(f"({t.offset}, {t.length}, '{t.next_char}')")
        else:
            print(f"({t.offset}, {t.length}, -)")

    decompressed = decompress_lz77(compressed)
    print(f"Decompressed string: {decompressed}")