import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
random.seed(1)

#
# Random vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random1"),       # player 1
#               agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.RandomAgent("random"),        # player 1
              aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game
outcome = g.go()

first_ties = []
first_losses = []
second_ties = []
second_losses = []
for i in range(50):
    random.seed(i)
    g = game.Game(7, 6, 4, agent.RandomAgent("random"), aba.AlphaBetaAgent("alphabeta", 4))
    outcome = g.go()
    if outcome == 0:
        second_ties.append(i)
    elif outcome == 1:
        second_losses.append(i)
    g = game.Game(7, 6, 4, aba.AlphaBetaAgent("alphabeta", 4), agent.RandomAgent("random"))
    outcome = g.go()
    if outcome == 0:
        first_ties.append(i)
    elif outcome == 2:
        first_losses.append(i)
print(first_ties, first_losses, second_ties, second_losses)
