#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>


#define FLAG_SIZE 32 // including NULL terminator
#define HEX_SIZE 9 
void generate_hex(char* flag, char* hex);

void load_flag(char* flag) {
    FILE* file = fopen("./flag.txt", "r");

    if (file == NULL) {
        perror("Failed to open flag file");
        exit(1);
    }

    fgets(flag, FLAG_SIZE, file);
    fclose(file);
}

int main()
{
    char* flag = malloc(FLAG_SIZE);
    load_flag(flag);
    // printf("%s\n", flag);
    char* hex = malloc(HEX_SIZE);
    generate_hex(flag, hex); // convert flag chars to corresponding hex digits
    // printf("%s\n", hex);

    char input[HEX_SIZE];
    printf("Your guess: \n");
    fflush(stdout);
    fgets(input, HEX_SIZE, stdin);
    input[strcspn(input, "\n")] = 0; // set newline to NULL
    if (strlen(input) != HEX_SIZE - 1)
    {
        printf("You can't even set the right length!");
        exit(1);
    }
    // printf("%s\n", input);

    for (int i = 0, j = HEX_SIZE - 2; i < HEX_SIZE; i++, j--)
    {
        // reverse check
        if (input[j] != hex[i])
        {
            // printf("%d != %d\n", input[j], hex[i]);
            printf("Wrong! You can't beat me. Goodbye!\n");
            exit(1);
        }
        // sleep on match
        usleep(250000);
    }

    // print flag on coming out of loop
    // which means all hex values have been matched in reverse
    printf("Congrats! You guessed (or shall we say timed?) Roomba's password right.\nHere's your flag: %s\n", flag);

    free(flag);
    free(hex);
}

// generate hex of middle 4 characters of the flag
// participants will do timing attack against 8 chars
void generate_hex(char* flag, char* hex)
{
    for (int i = 0, j = 6; j < 10; i += 2, j++)
    {
        sprintf(&hex[i], "%x", flag[j]);
    }
    hex[16] = '\0'; // hex = 74314d33
}
