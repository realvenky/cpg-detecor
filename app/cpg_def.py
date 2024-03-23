from typing import Sequence
from functools import partial
import random
import torch
import numpy as np
import random



# Model
class CpGPredictor(torch.nn.Module):
    ''' Simple model that uses a LSTM to count the number of CpGs in a sequence '''
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(CpGPredictor, self).__init__()
        # We do need a lstm and a classifier layer here but you are free to implement them in your way
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.embedding = torch.nn.Embedding(5, input_size)
        self.lstm = torch.nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.embedding(x)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
