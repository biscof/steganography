from PIL import Image


def get_available_bits(image):
    # Use every 8th bit out of 24 bits in the RGB color representation (3 bits per pixel).
    BITS_PER_PIXEL = 3
    total_pixels = image.size[0] * image.size[1]
    return BITS_PER_PIXEL * total_pixels


def replace_least_significant_bit(color, msg_bit):
    # Clear the least significant bit (LSB) to 0 using a mask (0xFE or 0b11111110 or 254).
    # Then replace the LSB (0) with a message bit.
    return (color & 0b11111110) | int(msg_bit)


def get_image_with_secret(image, message_binary):
    """
    This function takes an input image and a binary message. It iterates through the pixels of the image,
    replacing the LSBs of each color channel (Red, Green, Blue) with bits from the secret message.
    The embedding process stops when the entire message has been embedded.
    """
    width, height = image.size
    msg_len = len(message_binary)
    curr_msg_bit_index = 0

    for y in range(height):
        for x in range(width):
            if curr_msg_bit_index >= msg_len:
                break

            current_pixel = image.getpixel((x, y))

            # Convert the pixel tuple into a modifiable list.
            new_pixel = list(current_pixel)

            # Iterate through the color channels of the pixel and replace their LSBs.
            for color_index in range(3):
                if curr_msg_bit_index >= msg_len:
                    break
                new_color = replace_least_significant_bit(
                    new_pixel[color_index],
                    message_binary[curr_msg_bit_index]
                )
                new_pixel[color_index] = new_color
                curr_msg_bit_index += 1

            # Replace the pixel at the (x, y) position with the modified pixel.
            image.putpixel((x, y), tuple(new_pixel))

        if curr_msg_bit_index >= msg_len:
            break

    return image


def hide_message_main(image, message, end_token):
    """
    This function takes an input image and a text message and hides the message within the image using steganography.
    It appends an end token to the message to mark the message's end and then encodes the message to ASCII
    and converts it to binary. Once the image with the hidden secret is obtained, it is saved.
    """
    image_copy = image.copy()

    message += end_token
    message_ascii = message.encode("ASCII")
    message_binary = "".join([format(i, '08b') for i in message_ascii])

    # Get the available number of bits we can use to hide the message.
    available_bits = get_available_bits(image_copy)

    if len(message_binary) > available_bits:
        print("Error: The message is too long to hide within this image."
            "Please try a shorter message.")
        return

    image_with_secret = get_image_with_secret(image_copy, message_binary)
    image_with_secret.save("stego_image.bmp")


def extract_hidden_message_main(image, end_token):
    """
    This function extracts a hidden text message from the image using steganography.
    It iterates through the pixels of the image, extracting the least significant bits (LSB)
    from each color channel (RGB) to reconstruct the hidden message.
    The function continues extracting bits until it finds the end token.
    """
    current_char_bits = []
    message = ""
    width, height = image.size
    BITS_IN_CHAR = 8

    for y in range(height):
        for x in range(width):
            current_pixel_list = list(image.getpixel((x, y)))

            # Extract least significant bits (LSB) from color channels (RGB). 
            for color_index in range(3):
                lsb = current_pixel_list[color_index] & 1
                current_char_bits.append(lsb)

            # When we have enough bits in our list, we can join 8 bist to get the charater.
            if len(current_char_bits) >= BITS_IN_CHAR:
                char_code = int("".join(map(str, current_char_bits[:BITS_IN_CHAR])), 2)
                curr_char = chr(char_code)
                message += curr_char

                # Remove the first 8 bits from the list (we've already used them).
                current_char_bits = current_char_bits[BITS_IN_CHAR:]

                if end_token in message:
                    return message[:-len(end_token)]

    return message


if __name__ == "__main__":
    END_TOKEN = "!3ND"
    stego_option = -1
    print("Welcome to the Steganography Tool!\n"
        "Choose an option: Enter 0 to hide a message or 1 to extract a hidden message.")
    while True:
        try:
            stego_option = int(input())
            if stego_option == 0 or stego_option == 1:
                break
            else:
                print("Please enter your choice (0 or 1):")
        except ValueError:
            print("Invalid input. Please enter either 0 or 1.")

    image = None
    while True:
        file_name = input("Enter the name of the image file (e.g., 'image.jpg'):\n")
        try:
            image = Image.open(file_name)
            break
        except FileNotFoundError:
            print("Invalid file name provided or the file doesn't exist.")

    if stego_option == 0:
        message = input("Please input the message you want to hide:\n")
        hide_message_main(image, message, END_TOKEN)
        print("The stego image has been successfully saved as 'stego_image.bmp'.")
    elif stego_option == 1:
        hidden_msg = extract_hidden_message_main(image, END_TOKEN)
        print(f"Message successfully extracted: {hidden_msg}")
    print("Thank you for using the Steganography Tool!")
