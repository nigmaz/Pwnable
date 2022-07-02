#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 512


long get_random() {
	return rand;
}

int get_version() {
	return 2;
}

int do_stuff() {
	long ans = (get_random() % 4096) + 1;
	int res = 0;
	
	printf("ans =%ld\n", ans);
	return res;
}

void win() {
	char winner[BUFSIZE];
	printf("New winner!\nName? ");
	gets(winner);
	printf("Congrats: ");
	printf(winner);
	printf("\n\n");
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	// Set the gid to the effective gid
	// this prevents /bin/sh from dropping the privileges
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	int res;
	
	printf("Welcome to my guessing game!\n");
	printf("Version: %x\n\n", get_version());
	
	for(int i = 0; i < 10; i++){
		res = do_stuff();
	}
	
	return 0;
}
