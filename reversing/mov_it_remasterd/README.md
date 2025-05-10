# mov it
```c
#include <stdio.h>
#include <unistd.h>

void main()
{
    int flag[] = {0x3a, 0x39, 0x70, 0x67, 0x32, 0x0f, 0x01, 0x5c, 0x45, 0x6c, 0x45, 0x00, 0x33, 0x2a, 0x72, 0x06, 0x20, 0x2b, 0x2e, 0x19, 0x77, 0x57, 0x2d, 0x09};
    char key[] = {'l', 'l', '3', '3', 't', 't'};
    int fd = open("./out", 1);
    int i;
    for (i = 0; i < 24; i++)
    {
        flag[i] ^= key[i % (sizeof(key) / sizeof(key[0]))];
    }

    for (i = 0; i < 24; i++)
    {
        flag[i] ^= key[i % (sizeof(key) / sizeof(key[0]))];
    }
    write(fd, flag, sizeof(int) * 24);
}

```