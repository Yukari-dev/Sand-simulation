from particle import Particle
from particles.wood import Wood
from particles.smoke import Smoke
import random

class Fire(Particle):
    def __init__(self):
        self.color = (255, random.randint(80, 160), 0)
        self.life = random.randint(30, 100)
    
    def update(self, sim, pos):
        self.life -= 1
        if self.life <= 0:
            sim.place_cell(pos, Smoke)
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for n in neighbors:
            cell = sim.peek_cell(pos, n)
            if isinstance(cell, Wood):
                target_pos = (pos[0] + n[0] * sim.resolution, pos[1] + n[1] * sim.resolution)
                sim.place_cell(target_pos, Fire)
        if self.life % 20:
            self.color = (255, random.randint(60, 180), 0)
        sim.is_dirty = True
