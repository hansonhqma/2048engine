# Python engine for 2048

Import and create engine with

```
from game import engine

instance = engine()
```

The size of the board is also adjustable with

```
instance = engine(_size = 6)
```

Interface with the engine using three functions
```
# direction: 'n', 's', 'e', 'w'
instance.move(direction)

# return game score
instance.score()

# reset game
instance.reset()

# you can also view the board by printing the game object
print(instance)
```

Alternatively play in the command line with `play.py` using WASD keys
