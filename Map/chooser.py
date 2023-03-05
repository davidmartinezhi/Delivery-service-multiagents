from random import randint

class Chooser: 
    def __init__(self, seq): 
        if not seq: 
            raise Exception()
        
        self.seq = seq
        self.bound = 0

    def choose(self): 
        if self.bound >= len(self.seq): 
            raise Exception()
        
        chosen = randint(self.bound, len(self.seq) - 1)
        item = self.seq[chosen]
        self.seq[self.bound], self.seq[chosen] = self.seq[chosen], self.seq[self.bound]
        self.bound += 1
        
        return item 