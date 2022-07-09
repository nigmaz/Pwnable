#include <stdlib.h> // Use After Free
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define BUFLEN 64

struct Dog //  char name[12] |  void (*bark)()  | void (*bringBackTheFlag)() | void (*death)(struct Dog *);
{
    char name[12];
    void (*bark)();
    void (*bringBackTheFlag)();
    void (*death)(struct Dog *);
};

struct DogHouse // char address[16] | char name[8]
{
    char address[16];
    char name[8];
};

int eraseNl(char *line) // replace newline = 0
{
    for (; *line != '\n'; line++)
        ;
    *line = 0;
    return 0;
}

void bark() // print 3 time repeat "UAF!!!" |2| |3|
{
    int i;
    for (i = 3; i > 0; i--)
    {
        puts("UAF!!!");
        sleep(1);
    }
}

void bringBackTheFlag() // print flag
{
    char flag[32];
    FILE *flagFile = fopen(".passwd", "r");
    if (flagFile == NULL)
    {
        puts("fopen error");
        exit(1);
    }
    fread(flag, 1, 32, flagFile);
    flag[20] = 0;
    fclose(flagFile);
    puts(flag);
}

void death(struct Dog *dog) // free(dog) |4|
{
    printf("%s run under a car... %s 0-1 car\n", dog->name, dog->name);
    free(dog);
}

// strncpy(dog->name, name, 12) | dog->bark = bark | dog->bringBackTheFlag = bringBackTheFlag | dog->death = death;
struct Dog *newDog(char *name) // init new dog in HEAP | struct Dog *dog = malloc(sizeof(struct Dog)); |1|
{
    printf("You buy a new dog. %s is a good name for him\n", name);
    struct Dog *dog = malloc(sizeof(struct Dog));
    strncpy(dog->name, name, 12);
    dog->bark = bark;
    dog->bringBackTheFlag = bringBackTheFlag;
    dog->death = death;
    return dog;
}

void attachDog(struct DogHouse *dogHouse, struct Dog *dog) // print dog->name live in address dogHouse->address |6|
{
    printf("%s lives in %s.\n", dog->name, dogHouse->address);
}

void destruct(struct DogHouse *dogHouse) // free(dogHouse) |7|
{
    if (dogHouse)
    {
        puts("You break the dog house.");
        free(dogHouse);
    }
    else
        puts("You do not have a dog house.");
}

// fgets line | eraseNL | strncpy(dogHouse->address, line, 16); | strncpy(dogHouse->name, line, 8); => init address[16] and name[8];
struct DogHouse *newDogHouse() // char line[BUFLEN] | struct DogHouse *dogHouse = malloc(sizeof(struct DogHouse)) |5|
{
    char line[BUFLEN] = {0};

    struct DogHouse *dogHouse = malloc(sizeof(struct DogHouse));

    puts("Where do you build it?");
    fgets(line, BUFLEN, stdin);
    eraseNl(line);
    strncpy(dogHouse->address, line, 16);

    puts("How do you name it?");
    fgets(line, 64, stdin);
    eraseNl(line);
    strncpy(dogHouse->name, line, 8);

    puts("You build a new dog house.");

    return dogHouse;
}

int main()
{
    int end = 0;
    char order = -1;
    char nl = -1;
    char line[BUFLEN] = {0};
    struct Dog *dog = NULL;
    struct DogHouse *dogHouse = NULL;
    while (!end)
    {
        puts("1: Buy a dog\n2: Make him bark\n3: Bring me the flag\n4: Watch his death\n5: Build dog house\n6: Give dog house to your dog\n7: Break dog house\n0: Quit");
        order = getc(stdin);
        nl = getc(stdin);
        if (nl != '\n')
        {
            exit(0);
        }
        fseek(stdin, 0, SEEK_END);
        switch (order)
        {
        case '1': // init dog
            puts("How do you name him?");
            fgets(line, BUFLEN, stdin);
            eraseNl(line);
            dog = newDog(line);
            break;
        case '2': // call dog->brak(); check (!dog)
            if (!dog)
            {
                puts("You do not have a dog.");
                break;
            }
            dog->bark();
            break;
        case '3': // print dog->name 12 char 2 time repeat | call dog->bark()
            if (!dog)
            {
                puts("You do not have a dog.");
                break;
            }
            printf("Bring me the flag %s!!!\n", dog->name);
            sleep(2);
            printf("%s prefers to bark...\n", dog->name);
            dog->bark();
            break;
        case '4': // call dog->death(dog) | free(dog)
            if (!dog)
            {
                puts("You do not have a dog.");
                break;
            }
            dog->death(dog);
            break;
        case '5': // init dogHouse
            dogHouse = newDogHouse();
            break;
        case '6': // print dog live in address
            if (!dog)
            {
                puts("You do not have a dog.");
                break;
            }
            if (!dogHouse)
            {
                puts("You do not have a dog house.");
                break;
            }
            attachDog(dogHouse, dog);
            break;
        case '7': // free(dogHouse)
            if (!dogHouse)
            {
                puts("You do not have a dog house.");
                break;
            }
            destruct(dogHouse);
            break;
        case '0':
        default:
            end = 1;
        }
    }
    return 0;
}
