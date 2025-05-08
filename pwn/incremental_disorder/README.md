## Incremental Disorder

Ideally they would notice:
1. The starting bytes are `8d 0d 04 08 eb 00` (`load ecx 0x00eb0804`) loading the string to print with the system call.
2. The buffer overflow with the read syscall where they can overwite the return address on the stack.
3. The dummy flag at address `0x08040d8d`.
4. The stray byte `b9` before the .text section / entry function that can reinterpret `b9 + 8d 0d 04 08 eb 00` as `mov ecx 0x08040d8d; jmp 00` (short jump at an offest of 0 = just continue).

So they just need to return to the byte before the .text section to print the flag.

This one-liner solves the challenge:

```bash
echo -ne "ABBBB\xFF\x0F\x04\x08" | ./inc
```