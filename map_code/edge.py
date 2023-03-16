class Edge: 
    def __init__(self, w = 0, w_bonus = 0):
        self.w = w
        self.w_bonus = w_bonus

    def get_w(self):
        return self.w + self.w_bonus  
    
    def mod_w(self, w_bonus): 
        self.w_bonus = w_bonus
    
    def restore(self): 
        self.w_bonus = 0
        