import random

puzzle_goal = [1, 2, 3, 4, 5, 6, 7, 0]
new_puzzles = []

f = open("./50puzzles/50puzzles.txt", "w")
for x in range(50):
    copy_puzzle = puzzle_goal
    random.shuffle(copy_puzzle)
    while ((not (copy_puzzle in new_puzzles)) and (copy_puzzle in [[1, 2, 3, 4, 5, 6, 7, 0], [1, 3, 5, 7, 2, 4, 6, 0]])):
        random.shuffle(copy_puzzle)
    new_puzzles.append(copy_puzzle)
    f.write(str(copy_puzzle).replace("[","").replace(",","").replace("]","") + "\n")
f.close()