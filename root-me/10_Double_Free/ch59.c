#include <stdlib.h> // Double Free
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// int hp | void (*hurt)() | void (*eatBody)() | void (*attack)() | int living;
struct Zombie
{
    int hp;
    void (*hurt)();
    void (*eatBody)();
    void (*attack)();
    int living;
};

// int hp | void (*fire)(int) | void (*prayChuckToGiveAMiracle)() | void (*suicide)() | int living;
struct Human
{
    int hp;
    void (*fire)(int);
    void (*prayChuckToGiveAMiracle)();
    void (*suicide)();
    int living;
};

struct Zombie *zombies[3];  // 3 zombies
struct Human *human = NULL; // 1 human

void fire(int zombieIndex) //|2|zombie->hp -= hits; if zombie->hp <= 0 -> memset zombie = 0 and FREE(zombies),zombies[zombieIndex] = NULL
{
    struct Zombie *zombie = zombies[zombieIndex]; // zombieIndex = order - 1
    int hits = rand() % 10;                       // hits = 0 -> 9
    printf("%d hits in his face\n", hits);
    zombie->hp -= hits;

    if (zombie->hp <= 0)
    {
        memset(zombie, 0, sizeof(struct Zombie));
        free(zombie);
        zombies[zombieIndex] = NULL;
        puts("The zombie die");
    }
    else
    {
        printf("The zombie has %d HP\n", zombie->hp);
    }
}

void prayChuckToGiveAMiracle() // print flag
{
    char flag[32] = {0};
    FILE *flagFile = fopen(".passwd", "r");
    if (flagFile)
    {
        fread(flag, 1, 32, flagFile);
        flag[20] = 0;
        sleep(5);
        puts("Chuck Norris arrives, kills every zombie like a boss. Turns back to you and says:");
        puts(flag);
    }
    exit(0);
}

void suicide() // free(human) - Human die |3|
{
    puts("You can't survive at this zombie wave. *PAM*");
    memset(human, 0, sizeof(struct Human));
    free(human);
}

// human->hp = 10 + rand() % 50 | human->fire = fire | human->prayChuckToGiveAMiracle = prayChuckToGiveAMiracle | human->suicide = suicide
// human->living = 1;
struct Human *newHuman() // init new human in HEAP | struct Human *human = malloc(sizeof(struct Human)); | 1 |
{
    puts("A new human arrives in the battle");
    struct Human *human = malloc(sizeof(struct Human));
    human->hp = 10 + rand() % 50;
    human->fire = fire;
    human->prayChuckToGiveAMiracle = prayChuckToGiveAMiracle;
    human->suicide = suicide;
    human->living = 1;
    return human;
}

void sound() // print - no care
{
    puts("Rhooarg...");
}

//  memset(zombie, 0, sizeof(struct Zombie)) | free(zombie) | zombies[zombieIndex] = NULL;
void eatBody(int zombieIndex) // |7|
{
    struct Zombie *zombie = zombies[zombieIndex];
    puts("The zombie eats an unfortunate mate, RIP bro");
    sleep(2);
    puts("But this bro hold a grenade in his hand... Good bye zombie");

    memset(zombie, 0, sizeof(struct Zombie));
    free(zombie);
    zombies[zombieIndex] = NULL;
}

// if (human->hp <= 0) => memset(human, 0, sizeof(struct Human)) | free(human) | human = NULL;
void attack() // human->hp -= hits | |6|
{
    int hits = rand() % 10;
    printf("The zombie hits you %d times\n", hits);
    human->hp -= hits;
    if (human->hp <= 0)
    {
        memset(human, 0, sizeof(struct Human));
        free(human);
        human = NULL;
        puts("You die");
    }
    else
    {
        printf("You have %d HP\n", human->hp);
    }
}

// zombie->hp = 10 + rand() % 40 | zombie->eatBody = eatBody | zombie->living = 1 | zombie->attack = attack;
struct Zombie *newZombie() // struct Zombie *zombie = malloc(sizeof(struct Zombie)); |5|
{
    puts("A new zombie arrives");
    struct Zombie *zombie = malloc(sizeof(struct Zombie));
    zombie->hp = 10 + rand() % 40;
    zombie->eatBody = eatBody;
    zombie->living = 1;
    zombie->attack = attack;

    return zombie;
}

char getChar() // input order and nl
{
    char nl;
    char ret = getc(stdin);
    nl = getc(stdin);
    if (nl != '\n')
    {
        puts("Only one char is requested");
        exit(0);
    }
    return ret;
}

int eraseNl(char *line) // replace newline = 0
{
    for (; *line != '\n'; line++)
        ;
    *line = 0;
    return 0;
}

int main()
{
    int end = 0;
    char order = -1;
    char nl = -1;
    char line[64] = {0};

    memset(zombies, 0, 3 * sizeof(struct Zombie *));

    while (!end)
    {
        puts("1: Take a new character\n2: Fire on a zombie\n3: Suicide you\n4: Pray Chuck Norris to help you\n5: Raise a new zombie\n6: A zombie attacks\n7: A zombie eats a body\n0: Quit");
        order = getChar(); // input order and newline
        switch (order)
        {
        case '1': // init human
            if (human)
            {
                puts("You have already a character");
            }
            else
            {
                human = newHuman();
            }
            break;
        case '2': // can free(zombie)
            if (human)
            {
                puts("Which zombie do you shoot? (1-3)");
                order = getChar() - 0x30;   // ascii 1 2 3
                if (order < 1 || order > 3) // check 1 2 3
                    puts("You miss all the target");
                else if (zombies[order - 1]) // zombies 0 1 2
                    human->fire(order - 1);  // call human->fire()
                else
                    puts("There isn't a zombie here");
            }
            else
            {
                puts("You're already dead");
            }
            break;
        case '3': // human die -> free(human)
            if (human)
            {
                human->suicide();
            }
            else
            {
                puts("You're already dead");
            }
            break;
        case '4': // if human ton tai -> free(human)
            if (human)
            {
                puts("You pray, you pray, you pray...\nAnd you see the zombie in front of you... \nYou die, you die, you die");
                memset(human, 0, sizeof(struct Human));
                free(human);
                human = NULL;
            }
            else
            {
                puts("You're already dead");
            }
            break;
        case '5': // init zombie
            puts("Which zombie arrives? (1-3)");
            order = getChar() - 0x30;
            if (order < 1 || order > 3)
            {
                puts("There are only 3 zombies slots on this road");
            }
            else if (zombies[order - 1] && zombies[order - 1]->living)
            {
                printf("Zombie %d is already here\n", order);
            }
            else // init zombies if it don't already here
            {
                zombies[order - 1] = newZombie();
            }
            break;
        case '6': // zombie attack() after when check zombies is living
            puts("Which zombie attacks? (1-3)");
            order = getChar() - 0x30;
            if (order < 1 || order > 3)
            {
                puts("There are only 3 zombie slots on this road");
            }
            else if (zombies[order - 1] && zombies[order - 1]->living)
            {
                if (human)
                {
                    zombies[order - 1]->attack();
                }
                else
                {
                    puts("You're already dead");
                }
            }
            else
            {
                puts("This zombie is already dead");
            }
            break;
        case '7': //  zombie eatBody() after when check zombies is living
            puts("Which zombie eats? (1-3)");
            order = getChar() - 0x30;
            if (order < 1 || order > 3)
            {
                puts("There are only 3 zombies slots on this road");
            }
            else if (zombies[order - 1])
            {
                zombies[order - 1]->eatBody(order - 1);
            }
            else
            {
                puts("This zombie is already dead");
            }
            break;
        case '0':
        default:
            end = 1;
        }
    }
    return 0;
}
