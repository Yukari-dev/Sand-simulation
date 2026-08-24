from particle import Particle
import random
import colorsys

class Water(Particle):
    def __init__(self):
        self.is_solid = False
        hue = random.randrange(181, 217) / 360.0
        light = 50.0 / 100.0
        satu = random.randrange(50, 100) / 100.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def update(self, sim, pos):
        if sim.peak_cell(pos, (0, 1)) is None:
            sim.move_particle(pos, (0, 1))
            return;
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.peak_cell(pos, (d, 1)) is None:
                sim.move_particle(pos, (d, 1))
                return
        for d in dirs:
            if sim.peak_cell(pos, (d, 0)) is None:
                sim.move_particle(pos, (d, 0))
                return
