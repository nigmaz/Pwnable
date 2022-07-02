#include<stdio.h>
#include<stdlib.h>

#define BUFSIZE 100

long get_random() {
	return rand() % BUFSIZE;
}

int main(){
	int i = 0;
	while(i < 10){
		printf("%d\n", get_random() + 1);
		i++;
	}
	return 0;
}
