#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

typedef void (*FuncPtr)(int);

// Define the struct
typedef struct __attribute__((packed)) {
    char letter[3];
    int num;
    FuncPtr printFunc;
} info;

void printMessage(int num);
void vuln();

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    info infoVar;
    infoVar.printFunc = printMessage;
    infoVar.num = 0x1569;
    printf("Enter the character you wish to store in my core: ");
    fflush(stdout);
    /*
    * vuln: taking 8-byte input in a 3-byte space.
    * will lead to overflowing last byte of printFunc function pointer
    */
    scanf("%lu", &infoVar.letter); // expected input: 10250545975395434817 (0x8e41414141414141), only first byte (0xee) matters
    infoVar.printFunc(infoVar.num);
}

void printMessage(int num)
{
    fflush(stdout);
    printf("Hello stranger!\nWould you like to know my favorite number? Here it is: %d\n", num);
}

void vuln()
{
    int len;
    char message[32];
    printf("Welcome Master! You are now inside Roomba's core.\nYour wish is my command. How lengthy is your wish, Master?\n");
    fflush(stdout);
    scanf("%d", &len); // expected input: 25
    if (len * 2 > 0x32)
    {
        printf("Sorry, Master! Its too lengthy for me to process. I am consumed by despair at my weakness, fading into oblivion...\n");
        exit(1);
    }
    getchar(); // dangling newline from last scanf

    printf("Okay Master! I can process that. What is it that you wish?\n");
    fflush(stdout);
    fgets(message, 32, stdin); // %13$p%14$p%15$p%21$p  to leak canary, stack, program addr and libc
    printf(message); // format string vuln
    printf("Would you please confirm your wish, Master?\n");
    fflush(stdout);
    read(0, message, len * 2); // allows overwriting last 2 bytes of RBP to pivot stack frame
}
