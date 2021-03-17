import queue
import math
import time
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


def distance_to_exit(positional_entity, wrld):
    return max(abs(positional_entity.x - wrld.exitcell[0]), abs(positional_entity.y - wrld.exitcell[1]))


def selfpreserving_look_for_character(wrld, monster, monster_range):
    for dx in range(-monster_range, monster_range+1):
        # Avoid out-of-bounds access
        if (monster.x + dx >= 0) and (monster.x + dx < wrld.width()):
            for dy in range(-monster_range, monster_range+1):
                # Avoid out-of-bounds access
                if (monster.y + dy >= 0) and (monster.y + dy < wrld.height()):
                    # Is a character at this position?
                    if wrld.characters_at(monster.x + dx, monster.y + dy):
                        return True, dx, dy
    # Nothing found
    return False, 0, 0


def selfpreserving_must_change_direction(wrld, monster):
    # Get next desired position
    (nx, ny) = monster.nextpos()
    # If next pos is out of bounds, must change direction
    if ((nx < 0) or (nx >= wrld.width()) or
        (ny < 0) or (ny >= wrld.height())):
        return True
    # If these cells are an explosion, a wall, or a monster, go away
    return (wrld.explosion_at(monster.x, monster.y) or
            wrld.wall_at(nx, ny) or
            wrld.monsters_at(nx, ny) or
            wrld.exit_at(nx, ny))


def in_danger_at(wrld, x, y):
    # Search for bomb about to go off and hit this space
    if wrld.bomb_at(x, y) and wrld.bombs[wrld.index(x, y)].timer <= 1:
        return True
    # For each orthogonal direction, look for bomb about to go off with no other bomb, exit, or wall in between
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for i in range(1, wrld.expl_range + 1):
            nx = x + i*dx
            ny = y + i*dy
            if not (0 < nx < wrld.width()) or not (0 < ny < wrld.height()) or \
                    wrld.wall_at(nx, ny) or wrld.exitcell == (nx, ny):
                break
            if wrld.bomb_at(nx, ny):
                if wrld.bombs[wrld.index(nx, ny)].timer <= 1:
                    return True
                else:
                    break
    for mlist in list(wrld.monsters.values()):
        for monster in mlist:
            if monster.name == "selfpreserving":
                if abs(x - monster.x) < 2 and abs(y - monster.y) < 2:
                    return True
            if monster.name == "aggressive":
                if abs(x - monster.x) < 3 and abs(y - monster.y) < 3 and \
                        not wrld.wall_at(__sign__(x - monster.x), __sign__(y - monster.y)):
                    return True
    return False


def __sign__(x):
    if x == 0.0:
        return 0
    return int(math.copysign(1, x))


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # if self.random_monster_in_range(wrld, 4):
        #     if self.smart_monster_in_range(wrld, 4):
        if self.random_monster_in_range(wrld, 5) or self.smart_monster_in_range(wrld, 5):
                # combination of minimax and expectimax
                start = time.time()
                print("miniexpectimax")
                self.miniexpectimax(wrld, 2, 5)
                print("selected input: (", self.dx, self.dy, self.maybe_place_bomb, "), Time elapsed: ", time.time() - start)
        #     else:
        #         print("expectimax")
        #         self.expectimax(wrld)
        # elif self.smart_monster_in_range(wrld, 4):
        #     print("minimax")
        #     self.minimax(wrld)
        elif not self.a_star(wrld):
            print("wall search")
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
        monsterList = iter(wrld.monsters.values())
        m = next(monsterList, 0)
        if (m == 0):
            return 0;
        if (m[0].name != "stupid"):
            m = next(monsterList, 0)
            if (m == 0 or m[0].name != "stupid"):
                return 0
        m = m[0]
        playerX = self.x
        playerY = self.y
        monsterX = m.x
        monsterY = m.y
        difX = abs(playerX - monsterX)
        difY = abs(playerY - monsterY)
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
                                if (e.tpe == Event.CHARACTER_FOUND_EXIT):
                                    self.move(dx, dy)
                                    return
                            if (b):
                                continue
                            value = self.expectimaxHelper(newwrld)
                            moveTuple = (value, dx, dy)
                            cMoves.append(moveTuple)
        pMax = -math.inf
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
                                        heuristic -= 10000#((wrld.height() + wrld.width()) / 2)
                                    elif (e.tpe == Event.CHARACTER_FOUND_EXIT):
                                        heuristic += 10000#(wrld.height() + wrld.width())
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
        monsterList = iter(wrld.monsters.values())
        m = next(monsterList, 0)
        if (m == 0):
            return 0;
        if (m[0].name == "stupid"):
            m = next(monsterList, 0)
            if (m == 0 or m[0].name == "stupid"):
                return 0
        m = m[0]
        playerX = self.x
        playerY = self.y
        monsterX = m.x
        monsterY = m.y
        difX = abs(playerX - monsterX)
        difY = abs(playerY - monsterY)
        if (difX <= distance and difY <= distance):
            return 1
        return 0

    def minimax(self, wrld):
        pass

    # based on pseudocode from class lecture
    def a_star(self, wrld):
        print("astar")
        start = wrld.index(self.x, self.y)
        exit_cell = wrld.exitcell
        frontier = queue.PriorityQueue()
        frontier.put((0, start))
        previous = {}
        cost_so_far = {}
        previous[start] = None
        cost_so_far[start] = 0
        while not frontier.empty():
            current = frontier.get()[1]

            if current == wrld.index(exit_cell[0], exit_cell[1]):
                # search reached exit: find first move
                while previous[current] != start:
                    self.set_cell_color(current % wrld.width(), current // wrld.width(), Fore.RED + Back.GREEN)
                    current = previous[current]
                # move in direction of first move
                self.move(current % wrld.width() - self.x, current // wrld.width() - self.y)
                return True

            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    current_x = current % wrld.width()
                    current_y = current // wrld.width()
                    if (0 <= current_x + x < wrld.width()) and \
                            (0 <= current_y + y < wrld.height()) and \
                            not (wrld.wall_at(current_x + x, current_y + y)) and \
                            not (wrld.explosion_at(current_x + x, current_y + y)) and \
                            not (in_danger_at(wrld, current_x + x, current_y + y)):
                        new_cost = cost_so_far[current] + 1
                        next_space = wrld.index(current_x + x, current_y + y)
                        if next_space not in cost_so_far or new_cost < cost_so_far[next_space]:
                            cost_so_far[next_space] = new_cost
                            priority = new_cost + max(abs(exit_cell[0] - current_x - x),
                                                      abs(exit_cell[1] - current_y - y))
                            frontier.put((priority, next_space))
                            previous[next_space] = current

        # if search failed to reach exit
        return False

    def miniexpectimax(self, wrld, depth, view_range):
        solution = self.miniexpectimax_node(wrld, 0, depth, 0, view_range)
        self.move(solution[1], solution[2])
        if solution[3]:
            self.place_bomb()

    # Returns an array of best value, dx taken, dy taken, whether bomb was placed
    def miniexpectimax_node(self, wrld, depth, max_depth, score_gained, view_range):
        me = wrld.me(self)
        # update score_gained and check for game end
        end_flag = False
        for e in wrld.events:
            if e.tpe == Event.BOMB_HIT_WALL:
                score_gained += 10
            elif e.tpe == Event.BOMB_HIT_MONSTER:
                score_gained += 50
            elif e.tpe == Event.CHARACTER_FOUND_EXIT:
                score_gained += 2*wrld.time
                end_flag = True
            elif e.tpe == Event.BOMB_HIT_CHARACTER or e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                end_flag = True
        # terminal states (uses no motion and no bomb placed as dummy values)
        if end_flag or (depth != 0 and in_danger_at(wrld, me.x, me.y)):
            return [score_gained+depth, 0, 0, False]  # if game ended, return score gained in search
        if not self.random_monster_in_range(wrld, view_range) and not self.smart_monster_in_range(wrld, view_range):
            # if escaped monsters, return score gained in search plus presumed score gained afterward from reaching the
            # exit in the fewest number of moves (without pathfinding e.g. assuming route isn't blocked),
            # or score gained from waiting until the time runs out.
            presumed_score = max(wrld.time, 2*(wrld.time - distance_to_exit(me, wrld)))
            return [score_gained+depth+presumed_score, 0, 0, False]
        if depth >= max_depth:
            # if at max depth, assume character succeeds in escaping on the next step
            presumed_score = max(wrld.time, 2*(wrld.time - distance_to_exit(me, wrld)) - 1)
            return [score_gained+depth+presumed_score, 0, 0, False]

        best = [-10000, 0, 0, False]  # value, dx, dy, b
        monsters = []
        for monster_list in list(wrld.monsters.values()):
            monsters += monster_list
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # check if direction is not out of bounds or blocked
                if (0 <= me.x + dx < wrld.width()) and \
                        (0 <= me.y + dy < wrld.height()) and \
                        not (wrld.wall_at(me.x + dx, me.y + dy)):
                    # iterate for when bomb is placed or not placed
                    for b in [True, False]:
                        # make character's move
                        me.move(dx, dy)
                        me.maybe_place_bomb = b
                        # recursively search for each monster's possible moves
                        nmonsters = monsters.copy()
                        nv = self.monster_node(wrld, depth, max_depth, score_gained, view_range, nmonsters)
                        # update best if necessary
                        if nv > best[0]:
                            best = [nv, dx, dy, b]
        return best

    def monster_node(self, wrld, depth, max_depth, score_gained, view_range, monsters):
        # if monsters list is empty, go to next step and continue the search
        if not monsters:
            nw = wrld.next()[0]
            # continue search on that board
            return self.miniexpectimax_node(nw, depth + 1, max_depth, score_gained, view_range)[0]
        # otherwise find out first monster's move and if random, iterate over the possibilities
        if monsters[0].name == "aggressive":
            return self.selfpreserving_monster_node(wrld, depth, max_depth, score_gained, view_range, monsters, 2)
        if monsters[0].name == "selfpreserving":
            return self.selfpreserving_monster_node(wrld, depth, max_depth, score_gained, view_range, monsters, 1)
        else:
            return self.stupid_monster_node(wrld, depth, max_depth, score_gained, view_range, monsters)

    def stupid_monster_node(self, wrld, depth, max_depth, score_gained, view_range, monsters):
        total = 0
        count = 0
        monster = monsters.pop(0)
        # For each walkable adjacent cell (including diagonals and not moving)
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if (monster.x + dx >= 0) and (monster.x + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if (monster.y + dy >= 0) and (monster.y + dy < wrld.height()):
                        # Is this cell walkable?
                        if not wrld.wall_at(monster.x + dx, monster.y + dy):
                            monster.move(dx, dy)
                            # iterate over rest of monsters
                            total += self.monster_node(wrld, depth, max_depth, score_gained, view_range, monsters)
                            count += 1
        return total/count

    def selfpreserving_monster_node(self, wrld, depth, max_depth, score_gained, view_range, monsters, monster_range):
        monster = monsters.pop(0)
        # If a character is in the neighborhood, go to it
        (found, dx, dy) = selfpreserving_look_for_character(wrld, monster, monster_range)
        if found and not selfpreserving_must_change_direction(wrld, monster):
            monster.move(dx, dy)
            # iterate over rest of monsters
            return self.monster_node(wrld, depth, max_depth, score_gained, view_range, monsters)
        # If monster is idle or must change direction, iterate over each safe direction
        if ((monster.dx == 0 and monster.dy == 0) or
                selfpreserving_must_change_direction(wrld, monster)):
            # Keep track of total value and number of options
            total = 0
            count = 0
            # For each neighboring safe cell (including diagonals and not moving)
            for dx in [-1, 0, 1]:
                # Avoid out-of-bounds access
                if (monster.x + dx >= 0) and (monster.x + dx < wrld.width()):
                    for dy in [-1, 0, 1]:
                        # Avoid out-of-bounds access
                        if (monster.y + dy >= 0) and (monster.y + dy < wrld.height()):
                            # Is this cell safe?
                            if (wrld.exit_at(monster.x + dx, monster.y + dy) or
                                    wrld.empty_at(monster.x + dx, monster.y + dy)):
                                monster.move(dx, dy)
                                # iterate over rest of monsters
                                total += self.monster_node(wrld, depth, max_depth, score_gained, view_range, monsters)
                                count += 1
            if count:
                # Return average of possible values
                return total/count
            else:
                # Accept death
                monster.move(0, 0)
        # iterate over rest of monsters
        return self.monster_node(wrld, depth, max_depth, score_gained, view_range, monsters)

    def wall_search(self, wrld):
        solution = self.wall_search_node(wrld, 0, 3)
        self.move(solution[1], solution[2])
        if solution[3]:
            self.place_bomb()

    # Returns an array of best value, dx taken, dy taken, whether bomb was placed
    def wall_search_node(self, wrld, depth, max_depth):
        # terminal states (uses no motion and no bomb placed as dummy values)
        if game_end(wrld):
            return [-10000, 0, 0, False]  # if game ends its not because of reaching the exit in this case
        me = wrld.me(self)
        if depth >= max_depth:
            # if at max depth, return negative distance to exit as a heuristic
            value = -distance_to_exit(me, wrld)
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
