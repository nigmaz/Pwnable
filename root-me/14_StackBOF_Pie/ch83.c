#include <stdio.h>
#include <stdlib.h>
 
// Instructions //
// gcc -o  chall chall.c -Wl,-z,norelro -fno-stack-protector (on the app-systeme-ch61 server for instance, but the goal is to enable NX and PIE)
 
 
void Winner() {
    printf("Access granted!\n");
    FILE *fp;
    int c;
    fp = fopen(".passwd", "r");
    if (fp == NULL)
    {
        perror("Error while opening the file.\n");
        exit(EXIT_FAILURE);
    }
    else {
        printf("Super secret flag: ");
        while ((c = getc(fp)) != EOF)
            putchar(c);
        fclose(fp);
    }
}
 
int Loser() {
    printf("Access denied!\n");
    return 0;
}
 
int main() {
    char key[30];
    printf("I'm an unbreakable safe, so you need a key to enter!\n");
     printf("Hint, main(): %p\n",main);
     printf("Key: ");
     scanf("%s", &key);
     Loser();
    return 0;
}

// 	ssh -p 2223 app-systeme-ch83@challenge03.root-me.org


