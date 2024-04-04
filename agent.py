import torch
import torch.nn as nn
from game import engine
import random


class dqnagent:
    
    def __init__(self, _engine:engine):
        
        self.engine = _engine
        self.net = dqn()

        self.actions = ('n', 's', 'e', 'w')

    def get_state_tensor(self):
        return torch.from_numpy(self.engine.__STATE__.flatten()).type(torch.float32)
    
    def step(self, move:str) -> bool:
        return self.engine.move(move)
    

    # history includes:
    # state, action chosen, reward, new state, done



class dqn(nn.Module):
    """
    deep q network for 4x4 state
    """

    def __init__(self):
        super(dqn, self).__init__()

        self.fc1 = nn.Linear(16, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 16)
        self.fc4 = nn.Linear(16, 4)
        
    def forward(self, x:torch.tensor):
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = nn.functional.relu(self.fc3(x))
        x = nn.functional.relu(self.fc4(x))

        return x
