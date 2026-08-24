from particle import Particle

class Wood(Particle):
    def __init__(self):
        self.color = (133, 94, 66)
        self.is_solid = True

    def update(self, sim, pos):
        pass
