import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################


def result(brd, col):
    # Clone the original board
    nb = brd.copy()
    # Add a token to the new board
    # (This internally changes nb.player, check the method definition!)
    nb.add_token(col)
    return nb


# Check if a pair of identical tokens exists starting at (x,y) and in direction (dx,dy)
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# PARAM [int] dx: the step in the x direction
# PARAM [int] dy: the step in the y direction
# RETURN [int]: True if 2 tokens of the same type have been found, False otherwise
def is_pair(brd, x, y, dx, dy):
    """Return True if a pair of identical tokens exists starting at (x,y) and in direction (dx,dy)"""
    # Avoid out-of-bounds errors
    if x + dx >= brd.w or y + dy < 0 or y + dy >= brd.h:
        return 0
    # Get token at (x,y)
    t = brd.board[y][x]
    # Go through elements
    if t == 0 or brd.board[y + dy][x + dx] != t:
        return 0
    if t == brd.player:
        return 1
    return -1


# Check if a line of n-1 identical tokens exists starting at (x,y) and in direction (dx,dy)
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# PARAM [int] dx: the step in the x direction
# PARAM [int] dy: the step in the y direction
# RETURN [int]: True if n-1 tokens of the same type have been found, False otherwise
def is_one_short_line_at(brd, x, y, dx, dy):
    """Return True if a line of n - 1 identical tokens exists starting at (x,y) in direction (dx,dy)"""
    # Avoid out-of-bounds errors
    if x + (brd.n - 2) * dx >= brd.w or y + (brd.n - 2) * dy < 0 or y + (brd.n - 2) * dy >= brd.h:
        return 0
    # Get token at (x,y)
    t = brd.board[y][x]
    if t == 0:
        return 0
    # Go through elements
    for i in range(1, brd.n - 1):
        if brd.board[y + i*dy][x + i*dx] != t:
            return 0
    if t == brd.player:
        return 1
    return -1


# Check if a line of n-1 identical tokens exists starting at (x,y) and in direction (dx,dy)
#
# PARAM [int] x:  the x coordinate of the starting cell
# PARAM [int] y:  the y coordinate of the starting cell
# PARAM [int] dx: the step in the x direction
# PARAM [int] dy: the step in the y direction
# RETURN [int]: True if n-1 tokens of the same type have been found, False otherwise
def is_possible_win(brd, x, y, dx, dy):
    """Returns 1, or -1 if the current player, or other player respectively can still win in the line with length n,
    starting at (x,y) and in direction (dx,dy), and 0 otherwise"""
    # Avoid out-of-bounds errors
    if x + (brd.n - 1) * dx >= brd.w or y + (brd.n - 1) * dy < 0 or y + (brd.n - 1) * dy >= brd.h:
        return 0
    player = 1
    opponent = 1
    # Go through elements
    for i in range(brd.n - 1):
        if brd.board[y + i*dy][x + i*dx] == brd.player:
            opponent = 0
            if not player:
                return 0
        if brd.board[y + i*dy][x + i*dx] != 0:
            player = 0
            if not opponent:
                return 0
    return player - opponent


class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
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

    def max_value(self, brd, alpha, beta, depth, col):
        utility = self.utility(brd, depth, col)
        if utility is not None:
            # print(" " * depth + str(utility))
            return utility
        # print(" "*depth + "max: alpha: " + str(alpha) + ", beta: " + str(beta))
        value = -math.inf
        for next_col in brd.free_cols():
            value = max(value, self.min_value(result(brd, next_col), alpha, beta, depth + 1, col))
            if value > beta:
                # print(" " * depth + "value: " + str(value))
                return value
            alpha = max(alpha, value)
        # print(" " * depth + "value: " + str(value))
        return value

    def min_value(self, brd, alpha, beta, depth, col):
        utility = self.utility(brd, depth, col)
        if utility is not None:
            # print(" "*depth + str(-utility))
            return -utility  # Utility only is calculated in terms of the current player
        # print(" "*depth + "min: alpha: " + str(alpha) + ", beta: " + str(beta))
        value = math.inf
        for next_col in brd.free_cols():
            value = min(value, self.max_value(result(brd, next_col), alpha, beta, depth + 1, col))
            if value < alpha:
                # print(" " * depth + "value: " + str(value))
                return value
            beta = min(beta, value)
        # print(" " * depth + "value: " + str(value))
        return value

    def utility(self, brd, depth, col):
        outcome = brd.get_outcome()
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

    def heuristic(self, brd, col, depth):
        return 0

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ


class CenterHeuristicAgent(AlphaBetaAgent):
    def heuristic(self, brd, col, depth):
        return pow(-1, depth+1)*abs(brd.w / 2 - col - 0.5)/brd.w


class LineHeuristicAgent(AlphaBetaAgent):
    def heuristic(self, brd, col, depth):
        value = 0
        for x in range(brd.w):
            for y in range(brd.h):
                value += is_pair(brd, x, y, 0, 1)
                value += is_pair(brd, x, y, 1, 1)
                value += is_pair(brd, x, y, 1, 0)
                value += is_pair(brd, x, y, 1, -1)
        return value


class OneShortHeuristicAgent(AlphaBetaAgent):
    def heuristic(self, brd, col, depth):
        value = 0
        for x in range(brd.w):
            for y in range(brd.h):
                value += is_one_short_line_at(brd, x, y, 0, 1)
                value += is_one_short_line_at(brd, x, y, 1, 1)
                value += is_one_short_line_at(brd, x, y, 1, 0)
                value += is_one_short_line_at(brd, x, y, 1, -1)
        return value


class PossibleWinsHeuristicAgent(AlphaBetaAgent):
    def heuristic(self, brd, col, depth):
        value = 0
        for x in range(brd.w):
            for y in range(brd.h):
                value += is_possible_win(brd, x, y, 0, 1)
                value += is_possible_win(brd, x, y, 1, 1)
                value += is_possible_win(brd, x, y, 1, 0)
                value += is_possible_win(brd, x, y, 1, -1)
        return value


# THE_AGENT = PossibleWinsHeuristicAgent("Group23", 7) # <-- for 7x6 Connect 4
# THE_AGENT = PossibleWinsHeuristicAgent("Group23", 5) # <-- for 10x8 Connect 4
# THE_AGENT = CenterHeuristicAgent("Group23", 6) # <-- for 7x6 Connect 5
# THE_AGENT = CenterHeuristicAgent("Group23", 5) # <-- for 10x8 Connect 5
