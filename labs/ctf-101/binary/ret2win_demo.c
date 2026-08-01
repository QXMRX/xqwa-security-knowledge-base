#include <stdio.h>
#include <unistd.h>

void win(void) {
    puts("flag{local_ret2win_evidence}");
}

void read_training_input(void) {
    char buffer[32];
    puts("local training input:");
    read(STDIN_FILENO, buffer, 128);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    read_training_input();
    puts("normal return");
    return 0;
}
