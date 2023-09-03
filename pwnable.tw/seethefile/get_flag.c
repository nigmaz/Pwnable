#include <unistd.h>
#include <stdio.h>

int read_input(char *buf,unsigned int size){
    int ret ;
    ret = read(0,buf,size);
    if(ret <= 0){
        puts("read error");
        exit(1);
    }
    if(buf[ret-1] == '\n')
        buf[ret-1] = '\x00';
    return ret ;
}

int main(){
    char buf[100];
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    printf("Your magic :");
    read_input(buf,40);
    if(strcmp(buf,"Give me the flag")){
        puts("GG !");
        return 1;
    }
    FILE *fp = fopen("/home/seethefile/flag","r");
    if(!fp){
        puts("Open failed !");
    }
    fread(buf,1,40,fp);
    printf("Here is your flag: %s \n",buf);
    fclose(fp);
}
