## VacuSpy
Extract the SETUP from rtsp and create a script:

Crack it:
```py
import hashlib
import itertools
import string

# Digest auth parameters
username = "admin"
realm = "20bbbc5b553f"
nonce = "b78be1ee6734eab86679908265d2f0ee"
uri = "rtsp://192.168.1.220:554/H.264/trackID=1"
method = "SETUP"
expected_response = "e1acac580ec4cacb62c34e4ebd407908"

def md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

# Digest calculation
def compute_response(password):
    ha1 = md5_hash(f"{username}:{realm}:{password}")
    ha2 = md5_hash(f"{method}:{uri}")
    response = md5_hash(f"{ha1}:{nonce}:{ha2}")
    return response

def brute_force():
    chars = string.ascii_uppercase  # 'abcdefghijklmnopqrstuvwxyz'
    total = 26 ** 6
    for count, combo in enumerate(itertools.product(chars, repeat=6), 1):
        password = ''.join(combo)
        if compute_response(password) == expected_response:
            print(f"[+] Password found: {password}")
            return
        if count % 1000000 == 0:
            print(f"Checked {count}/{total} passwords...")
    # print(compute_response("UODDXH") == expected_response)

    print("[-] Password not found in keyspace.")

if __name__ == "__main__":
    brute_force()
```

Solve 
```sh
[+] Password found: UODDXH
python3 cracker.py  574.56s user 0.07s system 99% cpu 9:34.77 total
```

VUCTF{admin:UODDXH}