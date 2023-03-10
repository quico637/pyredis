from Parser import Parser

class Redis():

    def __init__(self, map={}) -> None:
        self.map = map

    def execute(self, str : str) -> str:

        cmd = Parser.parse(str=str)

        if not cmd:
            return


        if(cmd.cmd == "GET"):
            if cmd.args[0] not in self.map:
                return f"key {cmd.args[0]} NOT FOUND"
            return self.map[cmd.args[0]]

        elif(cmd.cmd == "SET"):
            self.map[cmd.args[0]] = cmd.args[1]
            return f"OK"
        elif(cmd.cmd == "DEL"):
            if cmd.args[0] not in self.map:
                return f"key {cmd.args[0]} NOT FOUND"
            del(self.map[cmd.args[0]])
            return "OK"