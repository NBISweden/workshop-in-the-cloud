#!/usr/bin/env python
import argparse

import yaml
import sys

import passlib.pwd
import passlib.hash


from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def create_ssh_key():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return (public_key.decode('utf-8'), private_key.decode('utf-8'))

def create_users(number):
    uid_start = 2000

    users = []
    for n in range(number):
        username = "user{:0>3}".format(n)
        password = passlib.pwd.genword(length=10)
        hash     = passlib.hash.sha512_crypt.using(rounds=5000).hash(password)
        uid      = uid_start + n

        public_key, private_key = create_ssh_key()

        users.append({
            "user": username,
            "password": password,
            "hash": hash,
            "uid": uid,
            "gid": uid,
            "private_key": private_key,
            "public_key": public_key,
        })

    return users

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('users', metavar='U', nargs='+', type=int, help='The number of users to generate credentials for')

    args = parser.parse_args()

    nusers = args.users[0]
    users = create_users(nusers)


    print(yaml.dump({"users": users}, default_flow_style=False))

if __name__ == '__main__':
    main()
