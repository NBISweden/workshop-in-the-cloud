#!/usr/bin/env python
import argparse

import passlib.pwd
import passlib.hash

import yaml
import sys


parser = argparse.ArgumentParser()
parser.add_argument('users', metavar='U', nargs='+', type=int, help='The number of users to generate credentials for')

args = parser.parse_args()

nusers = args.users[0]

users = []
for n in range(nusers):
    username = "user{:0>3}".format(n)
    password = passlib.pwd.genword(length=10)
    hash = passlib.hash.sha512_crypt.using(rounds=5000).hash(password)
    users.append({
        "user": username,
        "password": password,
        "hash": hash
    })


print(yaml.dump({"users": users}, default_flow_style=False))
