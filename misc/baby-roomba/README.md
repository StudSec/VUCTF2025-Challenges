# baby-roomba

Simple pyjail - Rombertus

## Solution

Built upon the fact that python2 input just executes code. 2 lines are in the far of distance on two
 other lines.

Simply do one exec to get the `NotImplementedError` which has a line hidden that executes
 `input = __builtins__.input` to set it to the unsafe input, after which you can simply just do
 `__import__("os").system("echo $FLAG")` to get the flag.
