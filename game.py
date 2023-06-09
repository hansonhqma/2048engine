import numpy as np
import random

class engine:
    
    def __init__(self, _size=4):

        self.__SIZE_CONST__ = _size
        self.__STATE__ = np.zeros((self.__SIZE_CONST__, self.__SIZE_CONST__)).astype(np.int32)
        self.__SCORE__ = 0
        self.__GAME_ACTIVE__ = True

        # insert two random tiles
        self.__insertrandomtile__()
        self.__insertrandomtile__()
        
        try:
            import torch
            self.__torch__ = torch
        except ModuleNotFoundError:
            self.__torch__ = None

    def move(self, direction) -> bool:
        # check move validity
        dir = direction.lower()

        prev_state = self.__STATE__.flatten()

        if dir == 'n' or dir == 's':
            self.__STATE__ = self.__STATE__.transpose()

        left_move = dir == 'w' or dir == 'n'
        
        self.__stack__(left=left_move)
        self.__compress__(left=left_move)
        self.__stack__(left=left_move)

        if dir == 'n' or dir == 's':
            self.__STATE__ = self.__STATE__.transpose()
        
        if np.array_equal(prev_state, self.__STATE__.flatten()):
            # invalid move
            return False

        self.__insertrandomtile__()

        if np.count_nonzero(self.__STATE__ == 0) == 0:
            self.__GAME_ACTIVE__ = False
        
        return True
    
    def score(self):
        return self.__SCORE__
    
    def active(self) -> bool:
        """
        returns whether or not the game is running or over
        """
        return self.__GAME_ACTIVE__

    def reset(self):
        self.__init__(_size=self.__SIZE_CONST__)

    def replicate(self):
        """
        return copy of game instance
        """
        
        copy = engine(_size = self.__SIZE_CONST__)
        copy.__STATE__ = self.__STATE__.copy()
        copy.__SCORE__ = self.__SCORE__
        copy.__GAME_ACTIVE__ = self.__GAME_ACTIVE__

        return copy
    
    def get_state_as_tensor(self):
        if not self.__torch__:
            print("Torch module not found")
            return None
        else:
            return self.__torch__.from_numpy(self.__STATE__.flatten().copy()).type(self.__torch__.float32)


    def __str__(self):
        return self.__STATE__.__str__()
    
    def __insertrandomtile__(self):
        if np.count_nonzero(self.__STATE__ == 0) > 0:
            # tiles spot available
            pos = self.__randomavailablecell__()
            value = 2 if random.uniform(0, 1) < 0.9 else 4
            
            self.__STATE__[pos[0], pos[1]] = value

    
    def __randomavailablecell__(self):
        # slow
        open_cell_pos = list(filter( lambda c : self.__STATE__[c[0], c[1]] == 0,
                                  [(x, y) for x in range(self.__SIZE_CONST__) for y in range(self.__SIZE_CONST__)]))
        
        return random.choice(open_cell_pos)
    
    def __stack__(self, left=True):
        for row in range(self.__SIZE_CONST__):
            if np.count_nonzero(self.__STATE__[row]) == self.__SIZE_CONST__:
                continue

            replacement_pos = 0 if left else self.__SIZE_CONST__-1
            start, stop, step = (0, self.__SIZE_CONST__, 1) if left else (self.__SIZE_CONST__-1, -1, -1)

            for col in range(start, stop, step):
                if self.__STATE__[row, col] != 0:
                    self.__STATE__[row, replacement_pos] = self.__STATE__[row, col]
                    if replacement_pos != col:
                        self.__STATE__[row, col] = 0
                    replacement_pos += 1 if left else -1

    def __compress__(self, left=True):
        for row in range(self.__SIZE_CONST__):
            start, stop, step = (0, self.__SIZE_CONST__-1, 1) if left else (self.__SIZE_CONST__-1, 0, -1)

            for col in range(start, stop, step):
                match = self.__STATE__[row, col] == self.__STATE__[row, col+1] if left else self.__STATE__[row, col] == self.__STATE__[row, col-1]

                if match:
                    new_value = self.__STATE__[row, col] + self.__STATE__[row, col+1] if left else self.__STATE__[row, col] + self.__STATE__[row, col-1]
                    self.__STATE__[row, col] = new_value
                    if left:
                        self.__STATE__[row, col+1] = 0
                    else:
                        self.__STATE__[row, col-1] = 0
                    self.__SCORE__ += new_value

