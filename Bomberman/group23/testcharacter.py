import queue
# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from events import Event
from colorama import Fore, Back
from sensed_world import SensedWorld


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
        if self.random_monster_in_range(wrld, 1):
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
        player = wrld.characters.keys()
        playerL = 0
        for i in player:
            playerL = i
        playerX = playerL % wrld.width()
        playerY = playerL // wrld.width()
        monster = wrld.monsters.keys()
        monsterL = 0
        for i in monster:
            monsterL = i
        monsterX = monsterL % wrld.width()
        monsterY = monsterL // wrld.width()
        difX = abs(playerX - monsterX)
        difY = abs(playerY - monsterY)
        print(difX)
        print(difY)
        if (difX <= 3 and difY <= 3):
            return 1
        return 0

    def expectimax(self, toClone):
        wrld = SensedWorld.from_world(toClone)
        cMoves = []
        c = next(iter(wrld.characters.values()))[0]
        # Loop through delta x
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (c.x + dx >= 0) and (c.x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    if (c.y + dy >= 0) and (c.y + dy < wrld.height()):
                        # No need to check impossible moves
                        if not wrld.wall_at(c.x + dx, c.y + dy):
                            # Set move in wrld
                            c.move(dx, dy)
                            # Get new world
                            (newwrld, events) = wrld.next()
                            b = 0
                            for e in events:
                                if (e.tpe == Event.CHARACTER_KILLED_BY_MONSTER):
                                    b = 1
                            if (b):
                                continue
                            value = self.expectimaxHelper(newwrld)
                            moveTuple = (value, dx, dy)
                            cMoves.append(moveTuple)
        pMax = -800
        i = 0
        index = 0
        for p in cMoves:
            if (p[0] > pMax):
                pMax = p[0]
                index = i
            i += 1
        self.move(cMoves[index][1], cMoves[index][2])

    def expectimaxHelper(self, wrld):
        m = next(iter(wrld.monsters.values()))[0]
        c = next(iter(wrld.characters.values()))[0]
        heuristic = 0
        # Loop through delta x
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (m.x + dx >= 0) and (m.x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (m.y + dy >= 0) and (m.y + dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(m.x + dx, m.y + dy):
                                # Set move in wrld
                                m.move(dx, dy)
                                # Get new world
                                (newwrld, events) = wrld.next()
                                for e in events:
                                    if (e.tpe == Event.CHARACTER_KILLED_BY_MONSTER):
                                        heuristic -= ((wrld.height() + wrld.width()) / 2)
                                    elif (e.tpe == Event.CHARACTER_FOUND_EXIT):
                                        heuristic += (wrld.height() + wrld.width())
                                mm = next(iter(newwrld.monsters.values()))[0]
                                difXcm = abs(c.x - mm.x)
                                difYcm = abs(c.y - mm.y)
                                difXce = abs(c.x - wrld.exitcell[0])
                                difYce = abs(c.y - wrld.exitcell[1])
                                difcm = difXcm + difYcm
                                curV = 0.2 * difcm - 0.1 * difXce - 0.7 * difYce
                                heuristic += curV
            return heuristic

    def smart_monster_in_range(self, wrld, distance):
        return 0

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
                    if (0 <= current_x + x < wrld.width()) and \
                            (0 <= current_y + y < wrld.height()) and \
                            not (wrld.wall_at(current_x + x, current_y + y)):
                        new_cost = cost_so_far[current] + 1
                        next_space = wrld.index(current_x + x, current_y + y)
                        if next_space not in cost_so_far or new_cost < cost_so_far[next_space]:
                            cost_so_far[next_space] = new_cost
                            priority = new_cost + max(abs(exit[0] - current_x - x), abs(exit[1] - current_y - y))
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
        # terminal states (uses no motion and no bomb placed as dummy values)
        if game_end(wrld):
            return [-10000, 0, 0, False]  # if game ends its not because of reaching the exit in this case
        me = wrld.me(self)
        if depth >= max_depth:
            # if at max depth, return negative distance to exit as a heuristic
            value = -max(abs(wrld.exitcell[0] - me.x), abs(wrld.exitcell[1] - me.y))
            if wall_in_danger(wrld):
                # prioritize walls in danger
                value += 1000
            return [value, 0, 0, False]

        # loop through all possible directions
        best = [-10000, 0, 0, False]  # value, dx, dy, b
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
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
                        nv = self.wall_search_node(nw, depth + 1, max_depth)[0]
                        # update best if necessary
                        if nv > best[0]:
                            best = [nv, dx, dy, b]
        return best


#loopy things
	current_x = x
	current_y = y
	    for add_x in [-1, 0, 1]:
                for add_y in [-1, 0, 1]:
                    
                    if (0 <= current_x+add_x < wrld.width()) and\
                            (0 <= current_y+add_y < wrld.height()) and\
                            not (wrld.wall_at(current_x+add_x, current_y+add_y)):
				#???
				#self.min_value(wrld, alpha, beta, current_x, current_y, 1)
                        

#from connect-n
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        value = -math.inf
        alpha = value
        best_cols = []
        # print("alpha: " + str(alpha) + ", beta: " + str(math.inf))
        for col in brd.free_cols():
            new_val = self.min_value(result(brd, col), alpha, math.inf, 1, col)
            print("col: " + str(col) + ", value: " + str(new_val))
            if new_val > value:
                value = new_val
                best_cols = [col]
            if new_val == value:
                best_cols.append(col)
            alpha = max(alpha, value)
        return best_cols[int((len(best_cols)-1)/2)]

    def max_value(self, wrld, alpha, beta, x, y, depth):
        utility = self.utility(wrld, x, y)
        if utility is not None:
            return utility
        value = -math.inf
	# something about moving differently        
	for next_col in brd.free_cols():
            value = max(value, self.min_value(result(brd, next_col), alpha, beta, depth + 1, col))
            if value > beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, brd, alpha, beta, x, y, depth):
        utility = self.utility(wrld, x, y)
        if utility is not None:
            return utility
        value = math.inf
	# something about moving differently
        for next_col in brd.free_cols():
            value = min(value, self.max_value(result(brd, next_col), alpha, beta, depth + 1, col))
            if value < alpha:
                # print(" " * depth + "value: " + str(value))
                return value
            beta = min(beta, value)
        return value


    def utility(self, wrld, x, y, depth):
	exit = wrld.exitcell
	if (x == exit[0]) && (x == exit[0])
	    return wrld.time
	elif game_end(wrld):
	    return -100;
	elif depth >= 3:
	    return -max(abs(exit[0]-x), abs(exit[1]-y)) # not the proper dist formula
	else
	    return None

