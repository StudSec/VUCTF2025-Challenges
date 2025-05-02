#include <stdio.h>
#include <poll.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>

#define PORT 7532
#define PASSWORD "lov2cl3an&suck"

int authorised = 0;
char buf[1024];

int setup_sock(){
    int fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in server_addr;

    if(fd < 0){
        printf("socket failed %d, %s \n", strerror(fd));
        exit(0);
    }
    printf("socket created successfully!\n");
    server_addr.sin_addr.s_addr = inet_addr("0.0.0.0");
    printf("done creating !\n");
    server_addr.sin_port = htons(PORT);
    server_addr.sin_family = AF_INET;

    printf("now binding!\n");
    if (bind(fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("bind failed %d, %s \n", strerror(errno));
        exit(0);
    }
    printf("socket bound successfully to port %d!\n", PORT);
    return fd;
}

void parse_cmd(char* buf){
    int configuration_params[32];
    int config_idx;
    memset(configuration_params, 0, sizeof(configuration_params));

    printf("msg started with %c\n", buf[0]);

    switch (buf[0])
    {
    case 'p':
        if(strcmp(buf + 2, PASSWORD) == 0){
            printf("authorised! you may now enter a new configuration file\n");
            authorised = 1;
        } else{
            printf("password wrong! (%s != %s)\n", buf + 2, PASSWORD);
        }
        break;
    case 'c':
        if (authorised == 1)
        {
            
            memcpy(&config_idx, buf + 2, sizeof(config_idx));

            printf("Configuration parameter update received %s of %d characters! for param %d: %d which used to be %d\n",
                buf, strlen(buf), config_idx, buf + 2 + sizeof(config_idx) + 1, configuration_params[config_idx]);
            memcpy(&(configuration_params[config_idx]), buf + 2 + 
                sizeof(config_idx) + 1, sizeof(configuration_params[config_idx]));

            
            int dev_null = open("/dev/null", O_WRONLY);
            write(dev_null, configuration_params, sizeof(configuration_params));
            close(dev_null);
            printf("configuration done!\n");
        }
        else{
            printf("you are not authorised to execute this command!\n");
        }
        
        break;
    case 'e':
        if (authorised == 1)
        {
            printf("exitting!\n");
            exit(0);
        }
        else{
            printf("you are not authorised to execute this command!\n");
        }
        break;
    default:
        printf("command not found!\n");
        break;
    }
    printf("returning\n");
}

int main(){
    int fd = setup_sock();
    struct pollfd pol_s;
    struct sockaddr_in client_addr = {};
    system("echo 'hi! please notice how system is available!'");

    while(1 == 1){
        memset(buf, 0, sizeof(buf));
        pol_s.fd = fd;
        pol_s.events = POLLIN | POLLERR;
        printf("polling started\n");
        poll(&pol_s, 1, -1);
        
        socklen_t client_addr_len = sizeof(client_addr);

        printf("woke up!\n");
        recvfrom(fd, buf, 1023, 0, (struct sockaddr*) &client_addr, &client_addr_len);
        char* client_ip_str = inet_ntoa(client_addr.sin_addr);
        printf("Received message from IP: %s and port: %i\n",
            client_ip_str, ntohs(client_addr.sin_port));

        if(strcmp(client_ip_str, "1.1.1.1") == 0){
            printf("MATCHED\n");
            parse_cmd(buf);
        }
    }

    close(fd);
}