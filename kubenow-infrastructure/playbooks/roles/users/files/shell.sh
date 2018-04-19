#!/bin/bash

NUM=${USER: -3}
COMPUTER=virt-workshop-node-$NUM
KEY=$HOME/.ssh/id_rsa
exec ssh -i $KEY $COMPUTER
