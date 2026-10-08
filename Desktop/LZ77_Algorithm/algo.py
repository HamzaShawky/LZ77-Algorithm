def lz77_encode(text):
    result = []
    position = 0

    while position < len(text):

        best_distance = 0
        best_length = 0

        for distance in range(1, position + 1):

            length = 0

            while (
                position + length < len(text)
                and text[position - distance + length] == text[position + length]
            ):
                length += 1

            if length > best_length:
                best_length = length
                best_distance = distance

        if best_length == 0:
            result.append([0, 0, text[position]])
            position += 1

        else:
            next_position = position + best_length

            if next_position < len(text):
                next_symbol = text[next_position]

                result.append([
                    best_distance,
                    best_length,
                    next_symbol
                ])

                position = next_position + 1

            else:
                result.append([
                    best_distance,
                    best_length,
                    None
                ])

                position = next_position

    return result


def lz77_decode(compressed):  
    text = ""

    for distance, length, next_symbol in compressed:

        for i in range(length):
            text += text[-distance]

        if next_symbol is not None:
            text += next_symbol

    return text


# User chooses the operation
choice = input("Choose 1 for Encode or 2 for Decode: ")


if choice == "1":

    text = input("Enter the text: ")

    result = lz77_encode(text)

    print("Encoded:")
    for item in result:
        print(item)


elif choice == "2":

    compressed = eval(input("Enter the encoded data: "))

    result = lz77_decode(compressed)

    print("Decoded:")
    print(result)


else:
    print("Invalid choice")

 # ABAABABBAAAB
 

 #ABAABABBAAAB 
