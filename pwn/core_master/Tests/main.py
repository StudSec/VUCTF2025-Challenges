#!/usr/bin/env python3.8

from pwn import *
import argparse
import filecmp
import json
import re
import os
import socket
import subprocess

context.log_level = 'error'

def run_test(flag, connection_string=None, handout_path=None, deployment_path=None, force_reusability=False):
    result = {}
    connection_string = connection_string[0] # We only have a single connection string
    host = connection_string.split(" ")[0]
    port = connection_string.split(" ")[1]

    # If the challenge is in good working order (DEPLOYMENT_WORKING)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex((host, int(port)))
    
    if (res == 0):
        sock.close()
        p = remote(host, int(port))
        resp = p.recvuntil(b": ")
        if "Enter the character you wish to store in my core:" in resp.decode('ascii'):
            result["DEPLOYMENT_WORKING"] = ""
        else:
            result["DEPLOYMENT_WORKING"] = "Challenge banner missing"
        p.close()    
    else:
        result["DEPLOYMENT_WORKING"] = "Connection failed"

    # If the original flag (passed as function parameter) and the received flag  match (FLAG_CORRECT)
    if result["DEPLOYMENT_WORKING"]:
        result["FLAG_CORRECT"] = "Unable to check flag"
    else:
        output = subprocess.run(['./solve.py', 'REMOTE'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Decodes bytes to str
            )
        # Split output into lines and get the last non-empty line
        output_lines = output.stdout.strip().split('\n')
        received_flag = output_lines[-1] if output_lines else ""
        # print(received_flag)
        
        if flag in received_flag:
            result["FLAG_CORRECT"] = ""
        else:
            result["FLAG_CORRECT"] = "Flag not found in output"

    # All required handout files are present, and match the deployment (HANDOUT_CORRECT)
    if not {"chall", "Dockerfile"}.issubset(set(os.listdir(handout_path))):
        result["HANDOUT_CORRECT"] = "Missing challenge binary or Dockerfile in handout"
    else:
        _, missmatch, _ = filecmp.cmpfiles(handout_path, deployment_path,
                                           ["challenge.c", "Dockerfile"], shallow=False)
        result["HANDOUT_CORRECT"] = ''.join(missmatch)


    # # Assert that all credentials/flags in the handout files are invalid (DUMMY_SECRET)
    # result["DUMMY_SECRET"] = grep_recursive("CTF{", handout_path)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the test with specified arguments.")

    parser.add_argument("--flag", type=str, required=True, help="The flag to run the test.")
    parser.add_argument("--connection-string", type=str, required=True, action='append',
                        help="The connection string in the form: \"<ip/hostname> <port>\"" +
                        "an example includes: --connection-string \"localhost 1337\" or" +
                        "--connection-string \"172.18.0.1 6564\"")
    parser.add_argument("--handout-path", type=str, required=True, help="The path" +
    " the /Handout dir of the challenge.")
    parser.add_argument("--deployment-path", type=str, required=True, help="The " +
    "path to the /Source directory of this challenge.")

    parser.add_argument("--force-reusability", action="store_true", help="This " +
    "flag is used when testing the challenge before it is given to the player."
    "After test is run with this flag, no artifacts should be left around"
    "that can affect the players experience")
    args = parser.parse_args()

    print(json.dumps(
        run_test(
            flag=args.flag,
            connection_string=args.connection_string,
            handout_path=args.handout_path,
            deployment_path=args.deployment_path,
            force_reusability=args.force_reusability
        )
    ))