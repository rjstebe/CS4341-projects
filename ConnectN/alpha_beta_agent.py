import math
import agent
import heuristics

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
        best_col = -1
        for col in brd.free_cols():
            new_val = self.min_value(result(brd, col), alpha, math.inf, 1)
            if new_val > value:
                value = new_val
                best_col = col
            alpha = max(alpha, value)
        return best_col

    def max_value(self, brd, alpha, beta, depth):
        utility = self.utility(brd, depth)
        if utility is not None:
            return utility
        value = -math.inf
        for col in brd.free_cols():
            value = max(value, self.min_value(result(brd, col), alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, brd, alpha, beta, depth):
        utility = self.utility(brd, depth)
        if utility is not None:
            return -utility  # Utility only is calculated in terms of the current player
        value = math.inf
        for col in brd.free_cols():
            value = min(value, self.max_value(result(brd, col), alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def utility(self, brd, depth):
        outcome = brd.get_outcome()
        if outcome == brd.player:
            return 1
        elif outcome != 0:
            return -1
        elif brd.free_cols() == 0:
            return 0
        elif depth >= self.max_depth:
            return heuristics.heuristic(brd)
        else:
            return None

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

# THE_AGENT = AlphaBetaAgent("Group23", 4)
