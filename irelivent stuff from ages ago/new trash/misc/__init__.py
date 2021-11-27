import os

import appdirs

user_data_dir = str(os.path.join(appdirs.user_data_dir(), "MemriseBot"))


def encode(string, key):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    encoded_string.replace("\n", "newline")
    return encoded_string


def decode(string, key):
    string.replace("newline", "\n")
    decoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        decoded_c = chr(ord(string[i]) - ord(key_c) % 256)
        decoded_chars.append(decoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string
