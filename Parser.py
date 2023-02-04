from Command import Command

def parse_key_only(args):
    
    if len(args) > 2 or len(args) <= 0:
        return None

    return args[1]

def parse_key_value(args):
    if len(args) > 3 or len(args) <= 0:
        return None

    return [args[1], args[2]]

def parse_cmd(args):
        
    if len(args) <= 0:
        return None

    return args[0]


class Parser():
    
    def parse(str) -> Command:

        args = str.split(" ")

        args = list(map(lambda s:s.strip(), args))

        cmd = parse_cmd(args=args)

        if len(args) > 3 or len(args) <= 0:
            return None

        if cmd == "SET":
            return Command(cmd, args[1:])

        if len(args) > 2:
            return None
        if cmd == "GET" or cmd == "DEL":
            return Command(cmd, args[1:])
        return None

