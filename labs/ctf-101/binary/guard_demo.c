#include <stdio.h>

int main(int argc, char **argv) {
    char buffer[32];
    const char *input = argc > 1 ? argv[1] : "training";
    int written = snprintf(buffer, sizeof(buffer), "%s", input);
    if (written < 0 || written >= (int)sizeof(buffer)) {
        puts("input too long");
        return 1;
    }
    printf("stored: %s\n", buffer);
    return 0;
}
