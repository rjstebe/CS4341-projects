# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group23')
from testcharacter import TestCharacter

# Create the game
#random.seed(1) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
#g.add_monster(SelfPreservingMonster("aggressive", # name
#                                    "A",          # avatar
#                                    3, 13,        # position
#                                    2             # detection range
#))

# TODO Add your character
#g.add_character(TestCharacter("me", # name
#                              "C",  # avatar
#                              0, 0  # position
# ))

# Run!
# g.go()




scores = []
results = []
for seed in range(0, 100):
    random.seed(seed)
    g = Game.fromfile('map.txt')
    
    g.add_monster(SelfPreservingMonster("aggressive",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        1  # detection range
                                        ))

     # TODO Add your character
    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

     # Run!
    g.go(1)
    scores.append(g.world.scores["me"])
    results.append(g.world.events)
win = 0
for score in scores:
    print(score)
for events in results:
    nevents = []
    for event in events:
        nevents.append(event.tpe)
        if (event.tpe == 4):
            win += 1
    print(nevents)
print(win)
