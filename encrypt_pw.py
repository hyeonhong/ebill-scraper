#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crypto import *
import argparse


def main():
    # key = generate_key()
    key = b'\x1df\xad\xfc\x95\x0f\x12B\xa7\xa3m\x14x\x86\x08\xa3'

    # encryption
    plaintext = parse_args().text
    encrypted_binary = encrypt(plaintext, key)
    encrypted_text = encrypted_binary.decode('latin-1')

    print("The encrpted text is generated below. \n\n{}".format(encrypted_text))


def parse_args():
    parser = argparse.ArgumentParser(description='Encrypts plaintext and returns the base64 value')
    parser.add_argument('--text', type=str, metavar='', help='Text to be encrypted (REQUIRED)', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
