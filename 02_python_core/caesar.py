import sys


def check_language(text):
    for char in text:
        if ord(char) > 127:
            raise Exception("The script does not support your language yet")


def caesar_cipher(text, shift, mode):
    check_language(text)
    result = []
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            offset = (ord(char) - base + shift * (1 if mode == 'encode' else -1)) % 26
            result.append(chr(base + offset))
        else:
            result.append(char)
    return ''.join(result)


def main():
    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments")

    mode = sys.argv[1]
    text = sys.argv[2]
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise Exception("Shift must be an integer")

    if mode not in ('encode', 'decode'):
        raise Exception("Mode must be either 'encode' or 'decode'")

    print(caesar_cipher(text, shift, mode))


if __name__ == '__main__':
    main()