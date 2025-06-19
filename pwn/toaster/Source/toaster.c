#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

void menu(){
    puts("Welcome to the roomba's toaster feature!");
    puts("-----------------------");
    puts("You can create your own toast here, but the toaster is a bit buggy.");
    puts("Even your fantasy toasts are perfectly fine!");
    puts("Buttt... the toaster needs to be pulled down in order to toast it.");
    puts("Can you manage to make the perfect toast?");
    puts("-----------------------");

}

void toast(){
    puts("You managed to make the perfect toast, please enjoy it!");
    if (setuid(0) != 0) {
        perror("setuid failed");
        return 1;
    }

    int fd = open("/flag.txt", O_RDONLY);
    if (fd < 0) {
        perror("open failed");
        return;
    }
    char flag[100] = {0};  // Zero-init
    int n = read(fd, flag, sizeof(flag) - 1);
    if (n <= 0) {
        perror("read failed");
        return;
    }
    write(1, "FLAG: ", 6);
    write(1, flag, n); 
    close(fd);
}

void kitchen(){
    char secret_recipe[24];

    printf("Please give me your secret recipe? \n");
    read(0, secret_recipe, 0x42);
}

void main(){
    menu();
    kitchen();
}