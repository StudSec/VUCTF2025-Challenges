import string

print("".ljust(80, "-"))
print("|" + "Welcome to Roomba C&C!".center(78) + "|")
print("|" + '"They\'ve grown old."'.center(78) + "|")
print("".ljust(80, "-"))
print("")


def get_banned():
    return [
        "help",
        "import",
        "eval",
        "exec",
        "os",
        "sys",
        "open",
        "chr",
        "system",
        "builtin",
        "subprocess",
        "pty",
        "popen",
        "read",
        "get_data",
        "'",
        "__",
        ".",
    ]


cmd = "1337"
while cmd != "exit":
    try:
        cmd = input(">>> ")
    
        if cmd == "exit":
            print("Goodbye!")
        elif cmd == "help":
            print("Commands: exit, help, update")
        elif len(cmd) > 5 and cmd[:6] == "update":
            print("Parsing update data...")
    
            if all(x in string.printable for x in cmd[7:]) and not any(x in cmd[7:] for x in get_banned()):
                print("Parse succesful, executing update...")
                exec(cmd[7:])
            else:
                raise ValueError("Update parsing failed!")
        else:
            print("Invalid command. Type 'help' for a list")
    except:
        cmd = "exit"
