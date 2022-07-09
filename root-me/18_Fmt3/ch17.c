#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
 
int main(int argc, char ** argv)
{
 
    // char    log_file = "/var/log/bin_error.log";
    char    outbuf[512];
    char    buffer[512];
    char    user[12];
 
    char *username = "root-me";
 
    // FILE *fp_log = fopen(log_file, "a");
 
    printf("Username: ");
    fgets(user, sizeof(user), stdin);
    user[strlen(user) - 1] = '\0';
 
    if (strcmp(user, username)) {
 
        sprintf (buffer, "ERR Wrong user: %400s", user);
        sprintf (outbuf, buffer);
        // fprintf (fp_log, "%s\n", outbuf);
   
        printf("Bad username: %s\n", user);
    }
   
    else {
 
        printf("Hello %s ! How are you ?\n", user);
    }
    // fclose(fp_log);
    return 0;
 
}

// 	ssh -p 2222 app-systeme-ch17@challenge02.root-me.org


