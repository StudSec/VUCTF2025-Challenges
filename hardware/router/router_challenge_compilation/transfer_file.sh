#!/bin/bash


transfer_file(){
FNAME=$1
scp $FNAME das5:~/
ssh openwrt scp cmt2314@fs0.das5.cs.vu.nl:~/$FNAME ./ -i /root/.ssh/id_dropbear
}

make clean
set -e
docker compose up --build

transfer_file ./router_challenge_static
transfer_file ./helloworld-std
