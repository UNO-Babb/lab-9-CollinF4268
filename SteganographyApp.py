# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image
import os

# Helper Functions
def numberToBinary(num):
    """Takes a base10 number and converts to a binary string with 8 bits"""
    binary = ""
    while num > 0:
        bit = num % 2
        binary = str(bit) + binary
        num = num // 2
    while len(binary) < 8:
        binary = "0" + binary
    return binary

def binaryToNumber(bin_str):
    """Takes a string binary value and converts it to a base10 integer."""
    decimal = 0
    exponent = 0
    for i in range(len(bin_str) - 1, -1, -1):
        if bin_str[i] == '1':
            decimal += 2 ** exponent
        exponent += 1
    return decimal

# Encode Function
def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    msgLength = len(msg)
    red, green, blue = pixels[0, 0]
    pixels[0,0] = (msgLength, green, blue)

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            greenBinary = greenBinary[0:7] + letterBinary[0]
            blueBinary = blueBinary[0:7] + letterBinary[1]
        elif pixel % 3 == 1:
            redBinary = redBinary[0:7] + letterBinary[2]
            greenBinary = greenBinary[0:7] + letterBinary[3]
            blueBinary = blueBinary[0:7] + letterBinary[4]
        else:
            redBinary = redBinary[0:7] + letterBinary[5]
            greenBinary = greenBinary[0:7] + letterBinary[6]
            blueBinary = blueBinary[0:7] + letterBinary[7]
            letterSpot = letterSpot + 1

        red = binaryToNumber(redBinary)
        blue = binaryToNumber(blueBinary)
        green = binaryToNumber(greenBinary)

        pixels[x,y] = (red, green, blue)
        pixel = pixel + 1

    img.save("secretImg.png", 'png')

# Decode Function
def decode(img):
    msg = ""
    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0
    while len(msg) < msgLength:
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]
        elif pixel % 3 == 1:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
        else:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
            letterAscii = binaryToNumber(letterBinary)
            msg = msg + chr(letterAscii)

        pixel += 1
        x = pixel % width
        y = pixel // width
    return msg

# Main Function
def main():
    print("Welcome to the Steganography App!")
    choice = input("Would you like to (e)ncode or (d)ecode a message?: ").lower()

    if choice == "e":
        image_name = input("Enter the name of the PNG image file to encode (e.g., pki.png): ")
        message = input("Enter the message to encode: ")
        try:
            img = Image.open(image_name)
            encode(img, message)
            img.close()
            print("Message successfully encoded into 'secretImg.png'")
        except Exception as e:
            print("Error:", e)

    elif choice == "d":
        image_name = input("Enter the name of the PNG image file to decode (e.g., secretImg.png): ")
        try:
            img = Image.open(image_name)
            message = decode(img)
            img.close()
            print("Decoded message:", message)
        except Exception as e:
            print("Error:", e)

    else:
        print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")

# Run main
if __name__ == '__main__':
    main()