#include <stdio.h>
#include <stdlib.h>

int classify(int value) {
    if (value > 10) {
        return value * 2;
    }
    return value - 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        puts("usage: ./classify NUMBER");
        return 1;
    }
    printf("%d\n", classify(atoi(argv[1])));
    return 0;
}
