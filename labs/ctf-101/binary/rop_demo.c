#include <stdio.h>
#include <unistd.h>

void training_target(long marker) {
    if (marker == 0x43544631) {
        puts("flag{local_rop_call_evidence}");
    }
}

void read_training_input(void) {
    char buffer[40];
    read(STDIN_FILENO, buffer, 160);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("local ROP teaching binary");
    read_training_input();
    return 0;
}
