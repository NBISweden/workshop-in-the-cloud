#!/usr/bin/env python
import argparse

import yaml
import sys
import subprocess
import re
import os.path

import passlib.pwd
import passlib.hash

import jinja2

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def render_template(file, **kwargs):
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('.'))
    template = env.get_template(file)
    return template.render( **kwargs )


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


def create_users(args):
    users = args.users

    user_names = []

    if os.path.isfile(users):
        with open(users) as fh:
            for line in fh:
                user, *password = line.split()
                if not password:
                    password = [passlib.pwd.genword(length=10)]
                user_names.append([user, password[0]])
    else:
        for n in range(int(users)):
            password = passlib.pwd.genword(length=10)
            user_names.append(["user{:0>3}".format(n), password])

    uid_start = 2000
    users = {}
    for n, user in enumerate(user_names):
        (username, password) = user
        num      = "{:0>3}".format(n)
        host     = "{}-node-{}".format(args.cluster_prefix, num)
        hash     = passlib.hash.sha512_crypt.using(rounds=5000).hash(password)
        uid      = uid_start + n

        public_key, private_key = create_ssh_key()

        users[host] = [{
            "host": host,
            "user": username,
            "password": password,
            "hash": hash,
            "uid": uid,
            "gid": uid,
            "private_key": private_key,
            "public_key": public_key,
            "num": num
        }]

    return users


def generate_config_file(**args):
    with open('config.tfvars', 'w') as fh:
        fh.write(render_template('config.tfvars.jj2', **args))


def generate_vars_file(args, users, shared = []):
    data = {
        "cluster_prefix": args.cluster_prefix,
        "master_host": "{}-master-000".format(args.cluster_prefix),
        "master_ip": "{{ hostvars.get(master_host)[\"ansible_host\"] }}",
        "users": users,
        "shared": shared,
    }

    vars_file = 'playbooks/group_vars/all'

    with open(vars_file, 'w') as fh:
        fh.write(yaml.dump(data, default_flow_style=False))


def generate_users_file(users):
    with open('passwords.txt', 'w') as fh:
        for u in [u for host in users.values() for u in host]:
            fh.write("{}\t{}\n".format(u['user'], u['password']))


def find_external_network():
    p = subprocess.run(['./kn', 'openstack', 'network', 'list', '--external'], stdout=subprocess.PIPE)
    for line in p.stdout.decode('utf8').split("\r\n"):
        m = re.search(r'([a-f0-9-]+) \| (Public External IPv4 network)', line, re.IGNORECASE)
        if m:
            id = m.group(1)
            name = m.group(2)
            return (id, name)
    return


def check_environment():
    if not os.environ.get('OS_AUTH_URL', False):
        sys.stderr.write("ERROR: You need to source the openstack credentials file.\n")
        sys.exit(1)

    if not os.path.isfile('ssh_key'):
        subprocess.run("ssh-keygen -t rsa -N '' -f ssh_key")


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--users',
            dest='users',
            type=str,
            required=True,
            metavar='USERS',
            help='Either The number of users to generate credentials for or a file with usernames, one per line.'
        )
    parser.add_argument(
            '--cluster-prefix',
            dest='cluster_prefix',
            type=str,
            default='virt-workshop',
            metavar='<virt-workshop>',
            help='Cluster prefix for hostnames in openstack, default is virt-workshop'
        )
    parser.add_argument(
            '--master-flavor',
            dest='master_flavor',
            type=str,
            default='ssc.small',
            metavar='<ssc.small>',
            help='The openstack flavor for the master node, default is ssc.small'
        )
    parser.add_argument(
            '--master-disk-size',
            dest='master_disk_size',
            type=int,
            default=0,
            metavar='<0>',
            help='The disk size for the extra disk of the master node, in Gb, default is 0'
        )
    parser.add_argument(
            '--student-flavor',
            dest='student_flavor',
            type=str,
            default='ssc.small',
            metavar='<ssc.small>',
            help='The openstack flavor for the student nodes, default is ssc.small'
        )
    parser.add_argument(
            '--student-disk-size',
            dest='student_disk_size',
            type=int,
            default=10,
            metavar='<10>',
            help='The disk size for the extra disk of the student nodes, in Gb, default is 10'
        )
    parser.add_argument(
            '--shared-dir',
            dest='shared_dirs',
            type=str,
            default=[],
            action='append',
            metavar='<shared-dir>',
            help='Directory that should be shared from the master node to the compute nodes, can be repeated',
        )

    return parser.parse_args()


def main():
    check_environment()

    args = parse_command_line()

    users = create_users(args)
    (id,name) = find_external_network()

    node_count = len(users)

    generate_config_file(**vars(args), external_network_id=id, external_network_name=name, node_count=node_count)
    generate_vars_file(args, users, args.shared_dirs)
    generate_users_file(users)

    print("""Course setup is finished
 To spin up the cloud run: ./kn apply
 The usernames and passwords are in the file passwords.txt""")


if __name__ == '__main__':
    main()
