from game import engine

g = engine()

while g.__GAME_ACTIVE__:
    print(g.__STATE__)
    move = input("> ")
    g.move(move)