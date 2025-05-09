from pwn import *
import argparse
import filecmp
import json
import re
import os
import subprocess

context.log_level = 'error'

def run_test(flag, connection_string=None, handout_path=None, deployment_path=None):
    result = {}
    connection_string = connection_string[0] # We only have a single connection string
    print(connection_string)
    host = connection_string.split(":")[0]
    port = connection_string.split(":")[1]
    print(host + ":" + port)

    # If the challenge is in good working order (DEPLOYMENT_WORKING)
    p = remote(host, int(port))

    if "1 - launch new instance" in p.recvline().decode('ascii'):
        result["DEPLOYMENT_WORKING"] = ""
    else:
        result["DEPLOYMENT_WORKING"] = "Challenge banner missing"
    p.close()

    # If the deployed flag and the stored flag (pass as function parameter) match (FLAG_CORRECT)
    if result["DEPLOYMENT_WORKING"]:
        result["FLAG_CORRECT"] = "Unable to check flag"
    else:
        p = remote(host, int(port))

        #match = re.search(r"Win @ (0x[0-9a-fA-F]+)", p.recvline().decode("ascii"))
        # p.sendline(b'\x41'*64 + b'\x42'*8 + bytes.fromhex(match.group(1)[2:])[::-1])
        # output = p.recvall()
        # matches = re.findall( r"CTF\{.*?\}", output.decode("ascii"))

        p.sendlineafter(b"action? ", b"1") # launching new instance

        p.recvuntil(b"uuid:           ")
        uuid = p.recvline()

        p.recvuntil(b"rpc endpoint:   ")
        rpc_endpoint = p.recvline()

        p.recvuntil(b"private key:    ")
        private_key = p.recvline()

        p.recvuntil(b"setup contract: ")
        setup_contract = p.recvline()

        bashCommand = f"/home/shinxy/.foundry/bin/forge script script/Solve.s.sol --rpc-url {rpc_endpoint.decode().strip()} --tc Solve --broadcast"

        print(bashCommand)
        process = subprocess.call(bashCommand.split(), stdout=subprocess.PIPE, env={"SETUP": setup_contract.decode().strip(), "PRIV": private_key.decode().strip(), "SETUP": setup_contract.decode().strip()})


        p = remote(host, int(port))
        p.sendlineafter(b"action? ", b"3")
        p.sendlineafter(b"uuid please: ", uuid)
               
        output = p.recvall()
        matches = re.findall( r"CTF\{.*?\}", output.decode("ascii"))

        # print(output)

        if flag.encode() in output:
            result["FLAG_CORRECT"] = ""
        elif matches:
            result["FLAG_CORRECT"] = "Found different flag: " + " ".join(matches)
        else:
            result["FLAG_CORRECT"] = "Flag not found in output"

    # All required handout files are present, and match the deployment (HANDOUT_CORRECT)
    if not {"Bank.sol", "Coin.sol", "Setup.sol"}.issubset(set(os.listdir(handout_path))):
        result["HANDOUT_CORRECT"] = "Missing Bank.sol, Coin.sol or Setup.sol"
    else:
        _, missmatch, _ = filecmp.cmpfiles(handout_path, deployment_path,
                                           ["Bank.sol", "Coin.sol", "Setup.sol"], shallow=False)
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
                        help="The connection string.")
    parser.add_argument("--handout-path", type=str, required=True, help="The handout path.")
    parser.add_argument("--deployment-path", type=str, required=True, help="The deployment path.")

    args = parser.parse_args()

    print(json.dumps(
        run_test(
            flag=args.flag,
            connection_string=args.connection_string,
            handout_path=args.handout_path,
            deployment_path=args.deployment_path,
        )
    ))