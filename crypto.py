#!/usr/bin/env python
# -*- coding: utf-8 -*-
# required package - "pycryptodomex"
import log
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random

logger = log.init_logger(__name__)


def encrypt(plaintext, key):
    binary_data = plaintext.encode('utf-8')
    iv = Random.new().read(16)  # 16-bytes-long nonce

    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = iv + cipher.encrypt(binary_data)  # Add nonce in the front
    return base64.b64encode(encrypted)  # Encode binary data to printable ASCII characters


def decrypt(encrypted, key):
    binary_data = base64.b64decode(encrypted)  # Decode back to binary data
    iv = binary_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted = cipher.decrypt(binary_data[AES.block_size:])
    return decrypted


# key must be either 16, 24, or 32 bytes long
# for example:
# key length 16 = AES-128
# key length 24 = AES-192
# key length 32 = AES-256
def generate_key():
    rnd = Random.new()
    return rnd.read(16)  # 16 bytes long = AES-128
