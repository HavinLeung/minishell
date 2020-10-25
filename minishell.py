#!/usr/bin/python3
import os
from sys import stdin, stderr

def main():
    builtins = None

    def print_flush(*args, **kwargs):
        print(*args, flush=True, **kwargs)

    def eprint(*args, **kwargs):
        print_flush(*args, file=stderr, **kwargs)

    def sh_ls(args):
        if len(args) != 1:
            eprint("Usage: {}".format(args[0]))
        else:
            for path in os.listdir():
                print_flush(path)

    def sh_pwd(args):
        if len(args) != 1:
            eprint("Usage: {}".format(args[0]))
        else:
            print_flush(os.getcwd())

    def sh_cd(args):
        if len(args) != 2:
            eprint("Usage: {} DIR".format(args[0]))
        else:
            os.chdir(args[1])

    def sh_help(args):
        print_flush("Havin's minishell")
        print_flush("Builtins:")
        for name in builtins.keys():
            print_flush(" - {}".format(name))

    def sh_exit(args):
        exit(0)

    def launch(args):
        pid = os.fork()
        if (pid == 0):
            os.execvp(args[0], args)
            # child
        else:
            # parent
            pid, status = os.waitpid(pid, 0)

    def execute(args):
        if not args:
            return True
        if args[0] in builtins:
            return builtins[args[0]](args)
        return launch(args)

    def repl():
        while True:
            user = os.getenv("USER")
            print_flush('{} on mini_sh> '.format(user), end='')
            args = list(filter(bool, stdin.readline().strip().split()))
            execute(args)

    # optional: load .minishellrc

    builtins = {
            "ls":sh_ls,
            "pwd":sh_pwd,
            "cd":sh_cd,
            "help":sh_help,
            "exit":sh_exit
            }
    repl()
    # optional: shutdown/cleanup

if __name__ == '__main__':
    main()
