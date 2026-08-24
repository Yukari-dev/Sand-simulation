from particle import Particle
import random

class Smoke(Particle):
    def __init__(self):
        self.color = (160, 160, 170)
        self.life = random.randint(40, 90)
        self.is_solid = False

    def update(self, sim, pos):
        self.life -= 1
        if self.life <= 0:
            sim.place_cell(pos, None)
            return
        
        if sim.peek_cell(pos, (0, -1)) is None:
            sim.move_particle(pos, (0, -1))
            return
        
        if sim.peek_cell(pos, (0, -1)) is not None:
            sim.swap_particles(pos, (pos[0], pos[1] - sim.resolution))
            return
        
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.peek_cell(pos, (d, -1)) is None:
                sim.move_particle(pos, (d, -1))
                return
            elif sim.peek_cell(pos, (d, 0)) is None:
                sim.move_particle(pos, (d, 0))
                return
