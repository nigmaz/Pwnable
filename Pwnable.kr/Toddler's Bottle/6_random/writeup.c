#include<stdio.h>

int main(){
	int random = 0x6b8b4567;
	int pass = 0xdeadbeef;	
	int key;
	key = pass ^ random;
	printf("%x", key);
	return 0;
}
