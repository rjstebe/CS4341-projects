import queue
# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        self.aStar(wrld)
        pass

    def aStar(self, wrld):
        exit = wrld.exitcell
        frontier = queue.PriorityQueue()
        pass