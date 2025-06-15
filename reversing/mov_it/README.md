# Mov it

This program is obfuscated using the movfuscator:
https://github.com/xoreaxeaxeax/movfuscator

Before diving into the code, perform some basic checks to uncover any interesting information.

For example, run `strings` on the binary and search for the flag:
```
strings mov_it | grep VUCTF
```
This command will reveal the flag!