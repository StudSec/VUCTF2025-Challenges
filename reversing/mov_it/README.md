# Mov it
Well this is obfusticated with movfusticator
https://github.com/xoreaxeaxeax/movfuscator

```c
void main() {
    char flag[] = "VUCTF{x0rr_x0r_m0v_m0v}";
    char key[]  = { 'm', '0', 'v', '1', 't', 't' };
    int fd = open("out", 1);
    int i;
    for (i = 0; i < 24; i++) {
        flag[i] ^= key[i % (sizeof(key) / sizeof(key[0]))];
    }
    write(fd, flag, 24);
}

```

## solve 
```py
def main():
    known_plain = b'VUCTF{'

    with open("out", "rb") as f:
        enc = f.read()

    key = bytes([enc[i] ^ known_plain[i] for i in range(6)])

    print(f"Recovered key: {key} (as string: {key.decode(errors='ignore')})")

    full_flag = bytes([enc[i] ^ key[i % len(key)] for i in range(len(enc))])

    print("Decrypted flag:", full_flag.decode())

if __name__ == "__main__":
    main()

```

no good solve for this one 