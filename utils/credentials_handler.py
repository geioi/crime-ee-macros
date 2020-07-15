import json
import os

from cryptography.fernet import Fernet
from os import path


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key/secret.key", "wb") as key_file:
        key_file.write(key)

def load_key(path_to_key="key/secret.key"):
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open(path_to_key, "rb").read()

def encrypt_value(value):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_value = value.encode()
    f = Fernet(key)
    return f.encrypt(encoded_value)

def decrypt_value(encrypted_value, keyfile):
    """
    Decrypts an encrypted message
    """
    key = load_key(keyfile)
    f = Fernet(key)
    decrypted_value = f.decrypt(encrypted_value)

    return decrypted_value.decode()

def saveCredentials(username, password, token, filename='config.txt'):
    if not path.exists('key/'):
        os.mkdir('key/')
        generate_key()
    elif not path.exists('key/secret.key'):
        generate_key()

    data = {}
    data['username'] = username
    data['password'] = encrypt_value(password).decode('utf-8')
    data['token'] = encrypt_value(token).decode('utf-8')

    with open(filename, 'w') as outfile:
        outfile.seek(0)
        json.dump(data, outfile)

def getCredentials(filename='config.txt', keyfile="key/secret.key"):
    with open(filename) as infile:
        data = json.load(infile)

    data['password'] = decrypt_value(bytes(data['password'], 'utf-8'), keyfile)
    data['token'] = decrypt_value(bytes(data['token'], 'utf-8'), keyfile)

    return data['username'], data['password'], data['token']
