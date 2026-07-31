CC ?= cc
CFLAGS = -Wall -Wextra -g -O0

PROGRAMS = hello_binary classify memory_map stack_demo ret2win_demo guard_demo rop_demo

.PHONY: all clean

all: $(PROGRAMS)

hello_binary: hello_binary.c
	$(CC) $(CFLAGS) $< -o $@

classify: classify.c
	$(CC) $(CFLAGS) $< -o $@

memory_map: memory_map.c
	$(CC) $(CFLAGS) $< -o $@

stack_demo: stack_demo.c
	$(CC) $(CFLAGS) $< -o $@

ret2win_demo: ret2win_demo.c
	$(CC) $(CFLAGS) -fno-stack-protector -no-pie $< -o $@

guard_demo: guard_demo.c
	$(CC) $(CFLAGS) $< -o $@

rop_demo: rop_demo.c
	$(CC) $(CFLAGS) -fno-stack-protector -no-pie $< -o $@

clean:
	$(RM) $(PROGRAMS)
