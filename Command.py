from abc import ABC, abstractmethod
from Parser import *

class Command():
    def __init__(self, cmd, args) -> None:
        self.cmd = cmd
        self.args = args



