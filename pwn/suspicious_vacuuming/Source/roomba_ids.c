#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define CMD_BUF_SIZE 128

struct roomb_defense
{
    char is_custom;
    char name[20];
    char code[475];
    struct roomb_defense* next;
    struct roomb_defense* prev;
};

#define BPFSCRIPT_HEADING "#!/usr/bin/env bpftrace\n\
BEGIN{ \n\
@bpfpid = pid; \n\
} \n\
interval:s:2 { \n\
    exit(); \n\
} \n\
"

char buffer[100];

struct roomb_defense defenses[10];
struct roomb_defense* head;

void add_defense(int i){
    struct roomb_defense* def = &defenses[i];
    struct roomb_defense* curr = head;

    if (def->is_custom == 1)
    {
        printf("[!] custom defenses are not yet security-tested\n");
        return;
    }
    
    if (curr == NULL)
    {
        head = def;
        return;
    }
    while (curr->next != NULL)
    {
        curr = curr->next;
    }
    curr->next = def;
    def->prev = curr;
}

void remove_defense(int i){
    printf("[+] removing defense %d: next: (%p) prev (%p)\n  ", i, defenses[i].next, defenses[i].prev);
    if (defenses[i].prev != NULL)
    {
        defenses[i].prev->next = defenses[i].next;
    }

    if (defenses[i].next != NULL)
    {
        defenses[i].next->prev = defenses[i].prev;
    }
    if (head == &defenses[i])
    {
        head = defenses[i].next;
    }
    
}

void configure_defense(char *cmd, char* code){
    for (int i = 0; i < 10; i++)
    {
        if (defenses[i].name[0] == 0)
        {
            printf("[+] %s added at %d \n", cmd, i);
            strncpy(defenses[i].name, cmd, sizeof(defenses[i].name) - 1);
            strncpy(defenses[i].code, code, sizeof(defenses[i].code) - 1);
            return;
        }
    }
    printf("[X] too many defenses configured\n");
}

#define ANTI_CMD(CMD) "tracepoint:syscalls:sys_enter_execve\n\
{\n\
    if(comm == \""CMD"\") { \n\
        printf(\"[ALERT] "CMD" launched: %s (PID: %d, UID: %d)\\n\",\n\
        comm, pid, uid);\n\
    } \n\
}"

#define INSERT_COUNTERMEASURE(CMD)if (strcmp(cmd + 2, CMD) == 0) \
{ \
    configure_defense(CMD, ANTI_CMD(CMD));\
    printf("[+] configured %s\n", CMD);\
}

void handle_start(char* cmd) {
    struct roomb_defense* curr = head;
    printf("[+] Starting the IDS.\n");
    FILE* fp = fopen("/tmp/run.bt", "w");
    fprintf(fp, "%s\n", BPFSCRIPT_HEADING);

    while (curr != NULL)
    {
        fprintf (fp, "//%s\n %s\n", curr->name, curr->code);
        printf("//%s\n %s\n", curr->name, curr->code);
        
        if (curr->is_custom == 1)
        {
            printf("[!] ERROR: custom block somehow ended up in the defenses list!\n");
            exit(0);
        }
        curr = curr->next;
    }
    fclose(fp);

    printf("[+] invoking bpftrace\n");
    system("chmod +x /tmp/run.bt");
    system("/tmp/run.bt");

    printf("[!] goodbye!\n");
    exit(0);
}

void handle_configure(char* cmd) {
    INSERT_COUNTERMEASURE("/bin/sh")
    INSERT_COUNTERMEASURE("/usr/bin/socat")
    INSERT_COUNTERMEASURE("/usr/bin/nc")
    INSERT_COUNTERMEASURE("/bin/bash")
}

void handle_add_defense(char* cmd){
    long int i = 0;
    char* endptr;
    i = strtol(cmd + 2, &endptr, 10);
    if (i < 0 || i >= 10)
    {
        printf("   index out of range! must be between 0 and 10\n");
    }
    add_defense(i);
}

void handle_remove_defense(char* cmd){
    long int i = 0;
    char* endptr;
    i = strtol(cmd + 2, &endptr, 10);
    if (i < 0 || i >= 10)
    {
        printf("   index out of range! must be between 0 and 10\n");
    }
    remove_defense(i);
}

void handle_configure_custom(char* cmd){
    long int i = 0;
    char* endptr;
    i = strtol(cmd + 2, &endptr, 10);
    if (i < 0 || i >= 10)
    {
        printf("   index out of range! must be between 0 and 10\n");
        return;
    }

    defenses[i].is_custom = 1;
    struct roomb_defense* curr = head;

    strcpy(defenses[i].name, "custom");
    
    printf("please input the bpftrace code\n");
    size_t j = 0;
    
    for (; j < 475; j++)
    {
        int c = getc(stdin);
        if (c == EOF || c == '\n')
        {
            break;
        }
        defenses[i].code[j] = (char)c;
    }
    defenses[i].code[j] = '\0';
    printf("[*] Bpftrace code received %s\n", defenses[i].code);
}

void list_defs(){
    puts("[+] currently enabled defenses:\n  ");
    for (size_t i = 0; i < 10; i++)
    {
        printf("   (%li) %s\n", i, defenses[i].name);
    }
    
    struct roomb_defense* curr = head;
    while (curr != NULL)
    {
        printf("%s ", curr->name);
        curr = curr->next;
    }
    puts("\n");
    return;
}

int main() {
    char cmd[CMD_BUF_SIZE];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);


    printf("Welcome to the command loop. Type 'exit' or 'e' to quit.\n");
    struct roomb_defense def;
    printf("i: %p n: %p c: %p p: %p n: %p\n",&def.is_custom, &def.name, &def.code, &def.prev, &def.next);

    while (1) {
        list_defs();
        puts("> ");
        fflush(stdin);
        if (!fgets(cmd, sizeof(cmd), stdin)) {
            // EOF or error
            printf("[!] eof or error\n");
            break;
        }

        // Remove newline
        cmd[strcspn(cmd, "\n")] = '\0';

        // Convert to lowercase for case-insensitive matching
        for (int i = 0; cmd[i]; i++) {
            cmd[i] = (char)tolower((unsigned char)cmd[i]);
        }

        if (cmd[0] == 'e') {
            printf("[*] goodbye!.\n");
            break;
        } else if (cmd[0] == 's') {
            handle_start(cmd);
        } else if (cmd[0] == 'c') {
            handle_configure(cmd);
        } else if (cmd[0] == 'a') {
            handle_add_defense(cmd);
        } else if (cmd[0] == 'r') {
            handle_remove_defense(cmd);
        } else if (cmd[0] == 'q') {
            handle_configure_custom(cmd);
        } else {
            printf("[-] Unknown command: '%s'\n", cmd);
            break;
        }
    }

    printf("[*] goodbye!\n");
    return 0;
}
