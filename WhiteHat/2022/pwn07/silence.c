#include<stdio.h>

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char buf[16]; // [rsp+0h] [rbp-10h] BYREF

  sub_4011A4(a1, a2, a3);
  puts("Just a normal shell - make it easy :xD");
  read(0, buf, 1000uLL);
  close(1);
  close(2);
  return 0LL;
}

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char buf[16]; // [rsp+0h] [rbp-10h] BYREF

  sub_4011A4(a1, a2, a3);
  puts("Just a normal shell - make it easy :xD");
  read(0, buf, 1000uLL);
  close(1);
  close(2);
  return 0LL;
}

// attributes: thunk
ssize_t read(int fd, void *buf, size_t nbytes)
{
  return read(fd, buf, nbytes);
}

// attributes: thunk
int close(int fd)
{
  return close(fd);
}

