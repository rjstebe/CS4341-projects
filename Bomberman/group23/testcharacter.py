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

    # based on pseudocode from class lecture
    def aStar(self, wrld):
        start = wrld.index(self.x, self.y)
        exit = wrld.exitcell
        frontier = queue.PriorityQueue()
        frontier.put((0, start))
        previous = {}
        cost_so_far = {}
        previous[start] = None
        cost_so_far[start] = 0
        while not frontier.empty():
            current = frontier.get()[1]

            if current == wrld.index(exit[0], exit[1]):
                break

            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    current_x = current % wrld.width()
                    current_y = int(current / wrld.width())
                    if (0 <= current_x+x < wrld.width()) and\
                            (0 <= current_y+y < wrld.height()) and\
                            (wrld.empty_at(current_x+x, current_y+y) or\
                             wrld.exit_at(current_x+x, current_y+y)):
                        new_cost = cost_so_far[current] + 1
                        next_space = wrld.index(current_x+x, current_y+y)
                        if next_space not in cost_so_far or new_cost < cost_so_far[next_space]:
                            cost_so_far[next_space] = new_cost
                            priority = new_cost + max(abs(exit[0]-current_x-x), abs(exit[1]-current_y-y))
                            frontier.put((priority, next_space))
                            previous[next_space] = current

        while previous[current] != start:
            self.set_cell_color(current % wrld.width(), int(current / wrld.width()), Fore.RED + Back.GREEN)
            current = previous[current]

        self.move(current % wrld.width() - self.x, int(current / wrld.width()) - self.y)
