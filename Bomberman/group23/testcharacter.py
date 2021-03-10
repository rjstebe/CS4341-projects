import queue
# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from events import Event
from colorama import Fore, Back


def wall_in_danger(wrld):
    for e in wrld.events:
        if e.tpe == Event.BOMB_HIT_WALL:
            return True
    return False
    # for k, bomb in wrld.bombs.items():
    #     nw = wrld.next()[0]
    #     ev = nw.add_blast(bomb)
    #     for e in ev:
    #         if e.tpe == Event.BOMB_HIT_WALL:
    #             return True
    # return False


def game_end(wrld):
    # Time's up
    if wrld.time <= 0:
        return True
    # No more characters left
    if not wrld.characters:
        return True
    # Last man standing
    if not wrld.exitcell:
        count = 0
        for k, clist in wrld.characters.items():
            count = count + len(clist)
        if count == 0:
            return True
    return False


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        if self.random_monster_in_range(wrld, 3):
            if self.smart_monster_in_range(wrld, 3):
                # combination of minimax and expectimax, or reinforcement learning
                pass
            else:
                self.expectimax(wrld)
        elif self.smart_monster_in_range(wrld, 3):
            self.minimax(wrld)
        elif not self.a_star(wrld):
            self.wall_search(wrld)

        # expectimax: Mike
        # minimax: Sam
        # wall search: Ryan
        # minimax/expectimax or reinforcement learning: Later

        # minimax and expectimax looks at score + distance to exit
        # variant 2: expectimax when monster is within 3 spaces

        # variant 3: minimax when monster is within 3 spaces

        # variant 4: minimax when monster is within 3 spaces

        # variant 5: minimax/expectimax or reinforcement learning

        # scenario 2: when a_star fails, search to destroy next wall

    def random_monster_in_range(self, wrld, distance):
        pass

    def expectimax(self, wrld):
        pass

    def smart_monster_in_range(self, wrld, distance):
        pass

    def minimax(self, wrld):
        pass

    # based on pseudocode from class lecture
    def a_star(self, wrld):
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
                # search reached exit: find first move
                while previous[current] != start:
                    self.set_cell_color(current % wrld.width(), int(current / wrld.width()), Fore.RED + Back.GREEN)
                    current = previous[current]
                # move in direction of first move
                self.move(current % wrld.width() - self.x, int(current / wrld.width()) - self.y)
                return True

            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    current_x = current % wrld.width()
                    current_y = int(current / wrld.width())
                    if (0 <= current_x+x < wrld.width()) and\
                            (0 <= current_y+y < wrld.height()) and\
                            not (wrld.wall_at(current_x+x, current_y+y)):
                        new_cost = cost_so_far[current] + 1
                        next_space = wrld.index(current_x+x, current_y+y)
                        if next_space not in cost_so_far or new_cost < cost_so_far[next_space]:
                            cost_so_far[next_space] = new_cost
                            priority = new_cost + max(abs(exit[0]-current_x-x), abs(exit[1]-current_y-y))
                            frontier.put((priority, next_space))
                            previous[next_space] = current

        # if search failed to reach exit
        return False

    def wall_search(self, wrld):
        solution = self.wall_search_node(wrld, 0, 2)
        self.move(solution[1], solution[2])
        if solution[3]:
            self.place_bomb()

    # Returns an array of best value, dx taken, dy taken, whether bomb was placed
    # terminal state (for pruning)
    # depth starts at maximum depth and counts down, cutoff starts at 0
    def wall_search_node(self, wrld, depth, max_depth):
        print("depth: ",depth)
        # terminal states (uses no motion and no bomb placed as dummy values)
        if game_end(wrld):
            return [-10000,0,0,False]  # if game ends its not because of reaching the exit in this case
        me = wrld.me(self)
        if depth >= max_depth:
            # if at max depth, return negative distance to exit as a heuristic
            value = -max(abs(wrld.exitcell[0] - me.x), abs(wrld.exitcell[1] - me.y))
            if wall_in_danger(wrld):
                # prioritize walls in danger
                value += 1000
            return [value,0,0,False]

        # loop through all possible directions
        best = [-10000,0,0,False]  # value, dx, dy, b
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                # check if direction is not out of bounds or blocked
                if (0 <= me.x + dx < wrld.width()) and \
                        (0 <= me.y + dy < wrld.height()) and \
                        not (wrld.wall_at(me.x + dx, me.y + dy)):
                    # iterate for when bomb is placed or not placed
                    for b in [True, False]:
                        # make next board with given inputs
                        me.move(dx, dy)
                        me.maybe_place_bomb = b
                        nw = wrld.next()[0]
                        # continue search on that board
                        nv = self.wall_search_node(nw, depth+1, max_depth)[0]
                        # update best if necessary
                        if nv > best[0]:
                            best = [nv, dx, dy, b]
        return best

def utility(self, wrld):
	if game_end(wrld):
	    return -100;
	elif ___:
	    return wrld.time
	else:
	    return max(abs(exit[0]-current_x-x), abs(exit[1]-current_y-y))



        if outcome == brd.player:
            return 1000*self.max_depth/depth
        elif outcome != 0:
            return -1000*self.max_depth/depth
        elif not brd.free_cols():
            return 0
        elif depth >= self.max_depth:
            return self.heuristic(brd, col, depth)
        else:
            return None
