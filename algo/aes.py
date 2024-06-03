from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives import padding, hashes

import base64


def generate_aes_key(key):
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(key)
    return hasher.finalize()[:32]


def encrypt(plaintext, key):
    hashed_key = generate_aes_key(key.encode())

    padder = padding.PKCS7(128).padder()
    plaintext = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(AES(hashed_key), CBC(b'\x00' * 16))

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode()


def decrypt(ciphertext, key):
    hashed_key = generate_aes_key(key.encode())
    ciphertext_decoded = base64.b64decode(ciphertext)

    cipher = Cipher(AES(hashed_key), CBC(b'\x00' * 16))

    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext_decoded) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()

    return plaintext.decode()
