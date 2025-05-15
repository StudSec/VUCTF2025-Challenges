# Mov it revenge
Although this code is obfuscated with the movfuscator:
https://github.com/xoreaxeaxeax/movfuscator

It doesn’t matter, because you can find the key in the strings. You can recognize the encryption as XOR (it’s quite common), or you could reverse the binary. The previous mov_it flag also hinted at this!

## Solution
```py
key = bytes([
    ord(c) for c in 'l33t_G3ralt_0f_R1V1a_tH3_W1tch3r1'
])

with open("out", "rb") as f:
    enc = f.read()
    
enc = bytes(enc[i] for i in range(0, len(enc), 4))
flag = bytes([enc[i] ^ key[i] for i in range(len(enc))])

print("Decrypted flag:", flag.decode())
```
