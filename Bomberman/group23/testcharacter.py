import queue
# This is necessary to find the main code
import sys
import math

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
        # if self.random_monster_in_range(wrld, 1):
            # if self.smart_monster_in_range(wrld, 2):
                # print('AAAAAA')
                # combination of minimax and expectimax, or reinforcement learning
                # pass
            # else:
                # self.expectimax(wrld)
        if self.smart_monster_in_range(wrld, 4):
            print('BBBBB')
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

    def smart_monster_in_range(self, wrld, distance):
        return (self.random_monster_in_range(wrld, distance))

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
        if (difX <= distance and difY <= distance):
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





    def minimax(self, toClone):
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
                            value = self.minHelper(newwrld)
                            if (dy == 0 and dx == 0):
                                value = value - 1
                            moveTuple = (value, dx, dy)
                            cMoves.append(moveTuple)

        pMax = -100000
        i = 0
        index = 0
        for p in cMoves:
            print(str(p[0]) + " " + str(p[1]) + " " + str(p[2]))
            if (p[0] >= pMax):
                pMax = p[0]
                index = i
            i += 1
        print(index)
        self.move(cMoves[index][1], cMoves[index][2])

    def minHelper(self, wrld):
        m = next(iter(wrld.monsters.values()))[0]
        c = next(iter(wrld.characters.values()))[0]
        heuristic = 0
        distTuples = []
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
                                        heuristic -= 1000
                                    elif (e.tpe == Event.CHARACTER_FOUND_EXIT):
                                        heuristic += 1000
                                mm = next(iter(newwrld.monsters.values()))[0]
                                difXcm = abs(c.x - mm.x)
                                difYcm = abs(c.y - mm.y)
                                difcm = math.sqrt((difXcm * difXcm) + (difYcm * difYcm))
                                dist = (difcm, m.x, m.y)
                                distTuples.append(dist)

        pMin = 800
        i = 0
        index = 0
        for p in distTuples:
            if (p[0] <= pMin):
                pMax = p[0]
                index = i
            i += 1
        m.move(distTuples[index][1] - m.x, distTuples[index][2] - m.y)
        return self.maxHelper(wrld)


    def maxHelper(self, wrld):
        m = next(iter(wrld.monsters.values()))[0]
        c = next(iter(wrld.characters.values()))[0]
        heuristic = 0
        hTuples = []
        exit = wrld.exitcell
        event_found = 0
        print(str(c.x) + " " + str(c.y))
        # Loop through delta x
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if ((c.x + dx) >= 0) and ((c.x + dx) < wrld.width() - 1):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if ((c.y + dy) >= 0) and ((c.y + dy) < wrld.height() - 1):
                            # No need to check impossible moves
                            if not (wrld.wall_at(c.x + dx, c.y + dy)):
                                # Set move in wrld
                                c.move(dx, dy)
                                # Get new world
                                (newwrld, events) = wrld.next()
                                for e in events:
                                    if (e.tpe == Event.CHARACTER_KILLED_BY_MONSTER):
                                        heuristic -= 100000
                                        event_found = 1
                                    elif (e.tpe == Event.CHARACTER_FOUND_EXIT):
                                        heuristic = 100000
                                        event_found = 1

                                if (event_found == 0):
                                    cc = next(iter(newwrld.characters.values()))[0]
                                    difXcm = abs(cc.x - m.x)
                                    difYcm = abs(cc.y - m.y)
                                    
                                    xToExit = abs(exit[0]-cc.x)
                                    yToExit = abs(exit[1]-cc.y)
                                    distToExit = max(xToExit, yToExit )
                                    
                                    
                                    if (distToExit <= 3 or distToExit < max(difXcm, difYcm)):
                                        heuristic = 10000 - 1000 * distToExit + (abs(dx) + abs(dy)) + max(difXcm, difYcm) - xToExit- yToExit
                                    elif not (difXcm >= 4 or difYcm >= 4):
                                        heuristic = 1000 + 2 * self.emptyCellsAround(wrld, cc) - 0.5 * (distToExit) + 20 * max(difXcm, difYcm) + (abs(dx) + abs(dy)) - 10 * self.wallsAround(wrld, cc)
                                        if (difXcm <= 1 and difYcm <=1):
                                            heuristic = -10000
                                    
                                        # elif (distToExit < 6):
                                            # print("close to exit")
                                            # heuristic = 2000 - 6 * distToExit + 2 * (difXcm + difYcm) + 0.1 * (abs(dx) + abs(dy))
                                    else: 
                                        heuristic = 5000 - 1 * distToExit +  2 * self.emptyCellsAround(wrld, cc) - 2 * self.wallsAround(wrld, cc)
                                
                                h = (heuristic, dx, dy)
                                # print(h)
                                hTuples.append(h)

        pMax = -1000000
        i = 0
        index = 0
        for p in hTuples:
            if (p[0] > pMax):
                pMax = p[0]
                index = i
            i += 1

        return pMax

    def monster_in_range(self, difXcm, difYcm):
        if (difXcm <=2 and difYcm <= 2):
            return 1
        #elif (difYcm <=2 and difYcm == 0):
            #return 1
        #elif (difYcm == difXcm) and ((difYcm ==1) or (difYcm ==2)):
            #return 1
        else:
            return 0

    def emptyCellsAround(self, wrld, c):
        emptyAround = 0
        for dx in [-1, 0, 1]:
        # Avoid out-of-bound indexing
            if (c.x + dx >= 0) and (c.x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                     if (c.y + dy >= 0) and (c.y + dy < wrld.height()):
                          if (wrld.empty_at(c.x+ dx, c.y+dy)):
                               emptyAround += 1
        return emptyAround

    def wallsAround(self, wrld, c):
        walls = 0
        for dx in [-1, 0, 1]:
        # Avoid out-of-bound indexing
            if (c.x + dx >= 0) and (c.x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 1]:
                     if (c.y + dy >= 0) and (c.y + dy < wrld.height()):
                          if (wrld.wall_at(c.x + dx, c.y + dy)):
                               walls += 1
        return walls


