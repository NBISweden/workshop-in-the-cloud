#!/usr/bin/env python
import argparse
import yaml
import sys
import subprocess
import re
import os.path

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--remote-dir',
            dest='remote_dir',
            type=str,
            default='/data',
            metavar='<remote-dir>',
            help='Remote directory. For example: "--remote_dir /data"',
        )
    parser.add_argument(
            '--local-dir',
            dest='local_dir',
            type=str,
            default=[],
            action='append',
            metavar='<local-data>',
            help='Local directory to upload to NFS. For example: "--local-dir ./dir1 --local-dir /opt/dir2"',
        )

    return parser.parse_args()

def check_upload_dir(local_dir):
    """Make sure upload path exists"""
    for dir in local_dir:
        if os.path.exists(dir) == False:
            print("Aborting... {} must exist".format(dir))
            sys.exit()
        else:
            print("Path {} is valid".format(dir))
    return True

def check_environment():
    if not os.path.isfile('ssh_key'):
        sys.stderr.write("ERROR: Private ssh not present. Are you in the correct directory?\n")
        sys.exit(1)

def upload_to_master(local_dir,remote_dir):
    user = 'ubuntu'
    master_ip = ''
    with open('./inventory', 'r') as inventory:
        fc = inventory.read()
        m = re.search(r'\[master\]\n(.)+',fc,re.M)
        if m:
            master_ip = m.group().split('\n')[1].split()[1].split('=')[1]

    for dir in local_dir:
        subprocess.run(['rsync', '-e', 'ssh -i ssh_key', '-avrz', dir, '{}@{}:{}'.format(user,master_ip,remote_dir)])

def main():
    args = parse_command_line()

    check_upload_dir(args.local_dir)
    check_environment()
    print("""Performing upload of local directories {} to {}""".format(args.local_dir,args.remote_dir))
    upload_to_master(args.local_dir,args.remote_dir)


if __name__ == '__main__':
    main()
