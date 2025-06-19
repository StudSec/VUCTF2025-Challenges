#include <unistd.h>
#include <string.h>

void _(){
    __asm__(
    "mov %rdx, %rdi\nret\n"
    "pop %rdx\nret\n"
    "xor %rax, %rax\nret\n"
    "mov $0x3b, %eax\nret\n"
    "xor %r15, %r15\nret\n"
    "mov %r15, %rsi\nret\n"
    "pop %r15\nret\n"
    "syscall\nret\n"
    "pop %rdi\nret\n"
    "inc %rax\nret\n"
    );
}

int main() {
    char buffer[16];
    const char *msg = "Tell me my secret shutdown command: \n";
    write(1, msg, strlen(msg)); 
    read(0, buffer, 500);
    return 0;
}
