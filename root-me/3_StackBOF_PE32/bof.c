#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
 
#define DEFAULT_LEN 16
 
void admin_shell(void)
{
        system("C:\\Windows\\system32\\cmd.exe");
}
 
int main(void)
{
        char buff[DEFAULT_LEN] = {0};
 
        gets(buff);
        for (int i = 0; i < DEFAULT_LEN; i++) {
                buff[i] = toupper(buff[i]);
        }
        printf("%s\n", buff);
}

// ssh -p 2225 app-systeme-ch72@challenge05.root-me.org
