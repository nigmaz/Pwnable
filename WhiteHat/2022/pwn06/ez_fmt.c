#include<stdio.h>


int init(EVP_PKEY_CTX *ctx)
{
  int iVar1;
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  iVar1 = setvbuf(stderr,(char *)0x0,2,0);
  return iVar1;
}

int restricted_filter(char *str)
{
  size_t sVar1;
  int i;
  
  i = 0;
  while (sVar1 = strlen(str), (ulong)(long)i < sVar1) {
    switch(str[i]) {
    case 'A':
    case 'E':
    case 'F':
    case 'G':
    case 'X':
    case 'a':
    case 'd':
    case 'e':
    case 'f':
    case 'g':
    case 'i':
    case 'o':
    case 'p':
    case 's':
    case 'u':
    case 'x':
      puts("Invalid character :TT");
      return -1;
    default:
      i = i + 1;
    }
  }
  return 1;
}

void main(void)
{
  int iVar1;
  EVP_PKEY_CTX *in_RDI;
  char buf [80];
  
  init(in_RDI);
  puts("Welcome to My Echo Service :##");
  while( true ) {
    fgets(buf,0x50,stdin);
    iVar1 = restricted_filter(buf);
    if (iVar1 == -1) break;
    printf(buf);
  }
                    /* WARNING: Subroutine does not return */
  exit(1);
}