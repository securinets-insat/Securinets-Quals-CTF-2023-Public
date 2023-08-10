// gcc main.c -o main2 -no-pie -z relro -z now -static

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct info{
    char username[16];
    char description[128+16];
};

void menu(){
    puts("1. Set username");
    puts("2. Set description");
    puts("3. Quit");
}

void memMove(char *dst, char *src, size_t size){
    while(size--){
        *(dst++) = *(src++);
    }
}

unsigned long readInt(){
    char x[20];
    char *p;
    fgets(x, 20, stdin);
    return strtoul(x, &p, 10);
}

void readInput(char* buff, size_t size){
    for(int i=0; i<=size; i++){
        if((buff[i] = getc(stdin)) == '\n'){
            buff[i] = '\0';
            break;
        }
    }
    return;
}

void readUsername(struct info* user){
    char input[sizeof(user->username)];

    puts("Your username:");
    readInput(input, sizeof(user->username));

    memMove(user->username, input, sizeof(user->username));
    return;
}

void readDescription(struct info* user){
    char input[sizeof(user->description)];

    puts("Your description:");
    readInput(input, sizeof(user->description));

    memMove(user->description, input, sizeof(user->description));
    return;
}

int main(){
    int choice;
    struct info user;

    do{
        puts("1. Set username");
        puts("2. Set description");
        puts("3. Quit");
        
        choice = readInt();

        switch(choice){
            case 1:{
                readUsername(&user);
                break;
            }
            case 2:{
                readDescription(&user);
                break;
            }
            case 3:{
                break;
            }
            default:{
                puts("???");
            }
        }
    } while(choice != 3);
    return 0;
}
