from __future__ import print_function
from random import randint                                                                                                                                                                                                                                                                                                                                                                                                         ; input = raw_input

print("".ljust(80, "-"))
print("|" + "Welcome to Baby Roomba C&C!".center(78) + "|")
print("|" + '"They shall grow old."'.center(78) + "|")
print("".ljust(80, "-"))
print("")

cmd = "1337"
while cmd != "exit":
    try:
        cmd = input(">>> ")

        if cmd == "exit":
            print("Goodbye!")
        elif cmd == "count":
            print("{0} baby roombas being trained!".format(randint(50, 5000)))
        elif cmd[:4] == "exec":
            print("Executing command: {0}".format(cmd))
            # TODO: implement the actual C&C code to the babies..
            raise NotImplementedError("C&C exec")
        elif cmd == "help":
            print("Commands: exit, count, exec, help")
        else:
            print("Invalid command. Type 'help' for a list")
    except NotImplementedError:
        print("C&C faced exception, going into fail mode!")                                                                                                                                                                                                                                                                                                                                                ; input = __builtins__.input
    except:
        cmd = "exit"
