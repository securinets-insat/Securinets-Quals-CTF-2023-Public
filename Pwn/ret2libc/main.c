// gcc main.c -o main -m32 -no-pie

#include <stdio.h>

void setup(){
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
}

int main(){
    char buff[80];

    setup();
    puts("Is this solveable?");

    gets(buff);
}
