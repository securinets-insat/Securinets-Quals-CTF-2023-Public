// gcc services.c -o services2 -z relro -z now -fstack-protector -lseccomp

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <seccomp.h>

char* config[8];
int PORT;
void (*backupCall)();
void *backupCode;

long readInt(){
    char x[256];
    long res;    
    read(0, x, 255);
    res = atol(x);
    return res;
}

void printMenu(){
    puts("1. Read chat");
    puts("2. Update config");
    puts("3. Backup Messages");
    puts("4. Exit");
}

void readChat(){
    char fname[255-7];
    char line[255];
    char path[255] = "./chat/";

    puts("Chat ID:");
    scanf("%s[254]s", &fname);
    strcat(path, fname);

    if(strstr(path, "flag") != NULL){
        puts("Not allowed");
        exit(0);
    }

    FILE* f = fopen(path, "r");

    if(f == NULL)
    {
        puts("Error!");   
        exit(1);             
    }

    while(fgets(line, 255, f)){
        write(1, line, strlen(line));
    }

    fclose(f);
    puts("");
}

void updateConfig(){
    long ind;

    puts("Config index:");
    ind = readInt();
    if(ind < 0){
        puts("Invalid index.");
        return;
    }

    puts("New config: ");
    read(0, config+ind, 10);
}

void setup(){
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void backupMessages(){
    if(!backupCall){
        puts("Backup functionality isn't available yet.");
        return;
    }

    if(strcmp(config[2], "backup: 1") != 0){
        puts("Backup is disabled.");
        return;
    }

    backupCall();
}

void rules(){
    scmp_filter_ctx ctx = seccomp_init(SECCOMP_RET_ALLOW);

	seccomp_rule_add(ctx, SECCOMP_RET_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SECCOMP_RET_KILL, 322, 0);
    seccomp_rule_add(ctx, SECCOMP_RET_KILL, 56, 0);
    seccomp_rule_add(ctx, SECCOMP_RET_KILL, 57, 0);
    seccomp_rule_add(ctx, SECCOMP_RET_KILL, 58, 0);

	seccomp_load(ctx);
	seccomp_release(ctx);
}

int main(){
    setup();
    rules();
    backupCall = NULL;
    config[2] = NULL;
    
    // Work In Progress, dynamically load backup code from remote server.
    // This is a placeholder.
    backupCode = mmap(NULL, 8, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);

    while(1){
        printMenu();
        puts("Choice:");
        switch(readInt()){
            case 1:{
                readChat();
                break;
            }
            case 2:{
                updateConfig();
                break;
            }
            case 3:{
                backupMessages();
                break;
            }
            case 4:{
                exit(0);
            }
        }
    }
}
