# Mov it revenge
Well this is obfusticated with movfusticator
https://github.com/xoreaxeaxeax/movfuscator

```c
void main() {
    char flag[] = "VUCTF{m0v_1t_r3vrs3_m3}";
    char key[] = {
        'm', 'o', 'v', '_', 'i', 't', '_', 'r', 'e', 'v', '_', 'i', 't',
        '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    };
    int fd = open("out", 1);
    int i;
    for (i = 0; i < 24; i++) {
        flag[i] ^= key[i];
    }
    write(fd, flag, 24);
}

```

## solve 
```py
def main():
    # The known XOR key (same as in your C code)
    key = bytes([
        ord(c) for c in 'mov_it_rev_it_1234567890'
    ])

    # Read the encrypted flag from 'out'
    with open("out", "rb") as f:
        enc = f.read()

    # Sanity check: length should match
    if len(enc) != len(key):
        print("Error: file size doesn't match key length.")
        return

    # Decrypt: XOR each byte with the key
    flag = bytes([enc[i] ^ key[i] for i in range(len(enc))])

    # Print the flag as a string
    print("Decrypted flag:", flag.decode())

if __name__ == "__main__":
    main()


```

no good solve for this one yet