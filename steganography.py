from PIL import Image


def open_img(file_name):
    """
    Open and return an image file.
    """
    return Image.open(file_name)


def get_available_bits(img_size):
    """
    Get the available number of bits that we can use to store the payload.
    """
    # Get the overall number of bits,
    # by finding the area of the image in pixels (length * breadth),
    # then multiplying the result by 24.
    bits = 3 * (img_size[0] * img_size[1])

    # The header is already dealt with by the Pillow library,
    # so we DON'T need to subtract it.
    return bits


def replace_pixel(i, x, y, payload_bin, rgb_index, pixel_map):
    """
    Replaces pixels of the cover image,
    storing the payload in the least significant bit.
    """
    # All bits in the byte as a list.
    colour = list(bin(pixel_map[x, y][rgb_index])[2:])

    # Replace the least significant bit.
    colour[-1] = payload_bin[i]

    # Rejoin the bits together as one string.
    colour = "".join(colour)

    # Cast the string back to an integer.
    colour = int(colour, 2)

    # Increment the index.
    i += 1
    return colour, i


def construct_stego_img(img_size, payload_bin, cover_pixels, stego_pixels):
    i = 0
    for x in range(img_size[0]):
        for y in range(img_size[1]):
            msg_len = len(payload_bin)
            if i >= msg_len:
                stego_pixels[x, y] = cover_pixels[x, y]
            else:
                if i < msg_len:
                    new_r, i = replace_pixel(i, x, y,
                                             payload_bin, 0, cover_pixels)
                else:
                    new_r = cover_pixels[x, y][0]
                if i < msg_len:
                    new_g, i = replace_pixel(i, x, y,
                                             payload_bin, 1, cover_pixels)
                else:
                    new_g = cover_pixels[x, y][1]
                if i < msg_len:
                    new_b, i = replace_pixel(i, x, y,
                                             payload_bin, 2, cover_pixels)
                else:
                    new_b = cover_pixels[x, y][2]

                new_pixel = (new_r, new_g, new_b)
                stego_pixels[x, y] = new_pixel


def stego_hide_main(end_token, file_name):
    # Receive message from user input.
    payload = input("Please input a message to hide:\n")

    # Add the end token.
    payload += ascii(end_token)

    # Open the cover image and load into memory.
    cover_img = open_img(file_name)

    # Get the available space in bits.
    available_bits = get_available_bits(cover_img.size)

    # Get length of payload in bits.
    payload_ascii = payload.encode("ASCII")
    payload_bin = "".join([format(i, '08b') for i in payload_ascii])
    message_bit_length = 0
    try:
        message_bit_length = len(payload_bin) * 8
    except message_bit_length > available_bits:
        print("Error: message too long")

    # Cache the width and height of the image.
    width = cover_img.size[0]
    height = cover_img.size[1]

    # Create the stego image.
    stego_img = Image.new("RGB", (width, height))
    stego_img.save("stego_img.bmp")
    stego_pixels = stego_img.load()
    construct_stego_img(stego_img.size,
                        payload_bin,
                        cover_img.load(),
                        stego_pixels)
    stego_img.save("stego_image.bmp")


def stego_extract_main(end_token, file_name):
    message_whole = []
    message_split = []

    stego_img = open_img(file_name)
    width = stego_img.size[0]
    height = stego_img.size[1]

    stego_pixels = stego_img.load()

    for x in range(width):
        for y in range(height):

            # Iterating over each colour in RGB tuple.
            for colour in stego_pixels[x, y]:

                # if i < len(payload_bin):

                # Identifying the last bit in each colour's binary value.
                last_bit = list(bin(colour)[2:])[-1]

                # Appending each LSB as a string to a list of all LSBs.
                message_whole.append(last_bit)

    # Iterate the list of all LSBs.
    for i in range(0, len(message_whole), 8):

        # Split into lists of 8 bits, then merge into strings.
        # Convert string binary values into integers and then to ASCII symbols using chr().
        message_split.append(chr(int("".join(message_whole[i:i+8]), 2)))

    # Merge symbols from the message list into a string.
    message = "".join(message_split)
    return message[:message.index(end_token)]


if __name__ == "__main__":
    CONST_END_TOKEN = "!3ND"
    stego_state = -1
    input_success = False
    print("Enter 0 to hide a message. Enter 1 to extract a hidden message.")
    while input_success is False:
        try:
            stego_state = int(input())
            if stego_state == 0:
                file_name = input("\nPlease enter the file name.")
                stego_hide_main(CONST_END_TOKEN, file_name)
                input_success = True
            elif stego_state == 1:
                file_name = input("\nPlease enter the file name.")
                print("The hidden message is: ", stego_extract_main(CONST_END_TOKEN, file_name))
                input_success = True
            else:
                print("Please enter either 0 or 1.")
        except ValueError:
            print("Please enter either 0 or 1.")












