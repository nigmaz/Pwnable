#include <stdio.h>
int dword_60212C;

int options() // print options | not care
{
    return printf("1: Create account\n2: Login\n3: Logout\n4: Delete account\n5: Exit\n==>Your choice:");
}

unsigned int alarm() // set time real | not care
{
    setbuf(stdin, 0LL);
    setbuf(stdout, 0LL);
    setbuf(stderr, 0LL);
    signal(14, handler);
    return alarm(0x30D40u);
}

__int64 __fastcall read_input(void *a1, unsigned int a2) // read string if value in address of point = 10 set = 0
{
    int v3; // [rsp+1Ch] [rbp-4h]

    v3 = read(0, a1, a2);
    if (v3 < 0)
        exit(0);
    if (*((_BYTE *)a1 + v3 - 1) == 10)
        *((_BYTE *)a1 + v3 - 1) = 0;
    return (unsigned int)v3;
}

// v0 = time(0LL)   |   srand(v0)   |   v4 = rand() % 300;
int _atoi() // input guess if == v4 set v2 = 1 and set dword_60212C = 1
{
    char nptr[24]; // [rsp+0h] [rbp-20h] BYREF

    unsigned __int64 v2; // [rsp+18h] [rbp-8h]

    v2 = __readfsqword(0x28u);
    read_input(nptr, 0x10u);

    return atoi(nptr);
}

__int64 Create_account() // malloc (&ptr)[i] - account ; malloc v2 - password | [1]
{
    int i;             // [rsp+4h] [rbp-3Ch]
    char *v2;          // [rsp+8h] [rbp-38h]
    char haystack[40]; // [rsp+10h] [rbp-30h] BYREF

    unsigned __int64 v4; // [rsp+38h] [rbp-8h]
    v4 = __readfsqword(0x28u);

    for (i = 0; i <= 8 && (&ptr)[i]; ++i) // ptr ?
        ;
    if (i == 9)
    {
        puts("No more mem");
        return 0LL;
    }
    else
    {
        printf("Input your account:");
        read_input(haystack, 39LL);
        if (strstr(haystack, "Admin")) // if string input has "Admin" -> Wrong -> jump return
        {
            puts("Wrong name");
        }
        else
        {
            (&ptr)[i] = (char *)malloc(0x28uLL); // point ptr ?
            memcpy((&ptr)[i], haystack, 0x27uLL);
            printf("Input your password:");
            v2 = (char *)malloc(0x28uLL); // point internal
            read_input(v2, 39LL);
            (&qword_602140)[i] = v2;
            puts("Done");
        }
        return 0LL;
    }
}

__int64 Login()
{
    unsigned int v0;   // eax
    int v2;            // [rsp+4h] [rbp-3Ch]
    int i;             // [rsp+8h] [rbp-38h]
    int v4;            // [rsp+Ch] [rbp-34h]
    char haystack[40]; // [rsp+10h] [rbp-30h] BYREF

    unsigned __int64 v6; // [rsp+38h] [rbp-8h]
    v6 = __readfsqword(0x28u);

    printf("Input your account:");
    read_input(haystack, 0x27u);

    if (strstr(haystack, "Admin")) // can set v2 = 1 after set dword_60212C = 1;
    {
        printf("Input your password:");
        read_input(haystack, 0x27u);
        if (!strcmp(haystack, &s2)) // s2 ?
        {
            v0 = time(0LL);
            srand(v0);
            v4 = rand() % 300; // init v4 random

            if ((unsigned int)_atoi() == v4) // atoi read number guess
            {
                printf("Welcome Admin");
                v2 = 1;
            }
        }
    }
    else
    {
        for (i = 0; i <= 8; ++i)
        {
            if ((&ptr)[i])
            {
                if (!strcmp(haystack, (&ptr)[i]))
                {
                    printf("Input your password:");
                    read_input(haystack, 0x1Du);
                    if (!strcmp(haystack, (&qword_602140)[i]))
                    {
                        printf("Welcome %s\n", haystack);
                        return 0LL;
                    }
                }
            }
        }
    }

    if (v2 == 1)
    {
        puts("1");
        dword_60212C = 1;
    }
    else if (v2 == 2)
    {
        puts("2");
        dword_60212C = 2;
    }
    else
    {
        puts("0");
        dword_60212C = 0;
    }
    puts("Fail");
    return 0LL;
}

void Logout() // dword_60212C = 0; | [3]
{
    dword_60212C = 0;
}

__int64 Delete_account()
{
    int v1; // [rsp+Ch] [rbp-4h]

    v1 = atoi();
    if (v1 >= 0 && v1 <= 9)
    {
        if ((&ptr)[v1])
            free((&ptr)[v1]);
        if ((&qword_602140)[v1])
            free((&qword_602140)[v1]);
        dword_60212C = 0;
        puts("Done");
        return 0LL;
    }
    else
    {
        puts("Fail");
        return 0LL;
    }
}

int flag() // dword_60212C == 1 jump read and print flag
{
    int result;   // eax
    char v1;      // [rsp+7h] [rbp-9h]
    FILE *stream; // [rsp+8h] [rbp-8h]

    result = dword_60212C; // enternal variable
    if (dword_60212C == 1)
    {
        stream = fopen("flag", "r");
        if (stream)
        {
            while (1)
            {
                v1 = fgetc(stream);
                if (v1 == -1)
                    break;
                putchar(v1);
            }
            return fclose(stream);
        }
        else
        {
            puts("You win but no flag here, call some one for help!");
            return 0;
        }
    }
    return result;
}

void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
    int v3; // [rsp+4h] [rbp-Ch] BYREF
    // selection

    unsigned __int64 v4; // [rsp+8h] [rbp-8h]
    v4 = __readfsqword(0x28u);

    alarm(a1, a2, a3);

    puts("==========TOKEN==========");
    while (1)
    {
        options();
        __isoc99_scanf("%d", &v3);
        switch (v3)
        {
        case 1:
            Create_account();
            break;
        case 2:
            Login();
            break;
        case 3:
            Logout();
            break;
        case 4:
            Delete_account();
            break;
        case 5:
            puts("Bye");
            exit(0);
        case 6:
            flag(); // dword_60212C == 1 print flag
            break;
        default:
            continue;
        }
    }
}

// note dword_60212C