#include <stdio.h>
#include <string.h>

int check(const char *input) {
    return strcmp(input, "training") == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        puts("usage: ./hello_binary WORD");
        return 1;
    }
    puts(check(argv[1]) ? "accepted" : "rejected");
    return 0;
}
