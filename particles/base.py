import random


class Element:
    color = (255, 255, 255)
    is_solid = False
    flammable = False
    updated = False

    def update(self, sim, pos):
        pass


class StaticSolid(Element):
    pass


class MovableSolid(Element):
    def update(self, sim, pos):
        if sim.is_empty(pos, (0, 1)):
            sim.move_particle(pos, (0, 1))
            return
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.is_empty(pos, (d, 1)):
                sim.move_particle(pos, (d, 1))
                return


class Liquid(Element):
    viscosity = 1.0

    def update(self, sim, pos):
        if random.random() > self.viscosity:
            return

        if sim.is_empty(pos, (0, 1)):
            sim.move_particle(pos, (0, 1))
            return
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.is_empty(pos, (d, 1)):
                sim.move_particle(pos, (d, 1))
                return
        for d in dirs:
            if sim.is_empty(pos, (d, 0)):
                sim.move_particle(pos, (d, 0))
                return


class Gas(Element):
    is_solid = False

    def __init__(self):
        super().__init__()
        self.life = random.randint(15, 50)

    def update(self, sim, pos):
        self.life -= 1
        if self.life <= 0:
            sim.place_cell(pos, None)
            return
        if sim.is_empty(pos, (0, -1)):
            sim.move_particle(pos, (0, -1))
            return
        if random.random() < 0.4:
            return
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.is_empty(pos, (d, -1)):
                sim.move_particle(pos, (d, -1))
                return
            elif sim.is_empty(pos, (d, 0)):
                sim.move_particle(pos, (d, 0))
                return
