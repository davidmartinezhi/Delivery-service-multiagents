from random import random, randint, choice 

class TrafficManager(): 
    def __init__(self, map, street_positions, congested, min_traffic, max_traffic, max_num_jams = 5, jam_prob = 0.1, phase_duration = 100): 
        self.map = map
        self.street_positions = street_positions
        self.congested_streets = congested
        self.min_traffic = min_traffic
        self.max_traffic = max_traffic
        self.max_num_jams = max_num_jams
        self.jam_prob = jam_prob
        self.phase_duration = phase_duration
        self.in_peak_traffic = False
        self.curr_step = -1

        self.affected_streets = {}
        
    def update_traffic(self): 
        for street in self.affected_streets.keys(): 
            self.map.restore_street(street)
            self.affected_streets[street].pop()

        if self.in_peak_traffic: 
            for street in self.congested_streets: 
                traffic = randint(self.min_traffic, self.max_traffic)
                map.mod_street(street, traffic)
                self.affected_streets[street] = traffic 

        for _ in self.max_num_jams: 
            if self.jam_prob <= random(): 
                self.affected_streets[choice(self.streets)] = self.max_traffic

    def get_traffic(self): 
        return self.affected_streets

    def step(self): 
        self.curr_step += 1
        if self.curr_step % self.phase_duration == 0:
            self.in_peak_traffic = not self.in_peak_traffic
            self.update_traffic()