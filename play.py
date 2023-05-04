from game import engine

g = engine()

print(g.__STATE__)

movemap = {'w':'n', 'a':'w', 's':'s', 'd':'e'}
while g.__GAME_ACTIVE__:
    move = input("> ")
    if move not in movemap:
        print("invalid move")
        continue
    g.move(movemap[move])
    print(g.__STATE__)