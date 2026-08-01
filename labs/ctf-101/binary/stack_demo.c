#include <stdio.h>
#include <string.h>

int copy_training_input(const char *input) {
    char buffer[16];
    memcpy(buffer, input, strlen(input) + 1);
    printf("copied: %s\n", buffer);
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        puts("usage: ./stack_demo TEXT");
        return 1;
    }
    return copy_training_input(argv[1]);
}
