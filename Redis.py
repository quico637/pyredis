from Parser import Parser

class Redis():
    def __init__(self) -> None:
        self.map = {}

    def execute(self, str : str):

        cmd = Parser.parse(str=str)

        if(cmd.cmd == "GET"):
            return self.map[cmd.args[0]]

        elif(cmd.cmd == "SET"):
            self.map[cmd.args[0]] = cmd.args[1]
            return f"OK"
        elif(cmd.cmd == "DEL"):
            del(self.map[cmd.args[0]])
            return "OK"