#include <stdio.h>
#include <stdlib.h>

int global_value = 7;

int main(void) {
    int local_value = 11;
    int *heap_value = malloc(sizeof(*heap_value));
    if (heap_value == NULL) {
        return 1;
    }
    *heap_value = 13;
    printf("global=%p local=%p heap=%p\n",
           (void *)&global_value, (void *)&local_value, (void *)heap_value);
    free(heap_value);
    return 0;
}
