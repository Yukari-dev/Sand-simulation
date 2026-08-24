from particle import Particle
import random
import colorsys

class Sand(Particle):
    def __init__(self):
        self.is_solid = True
        hue = 0.13
        light = random.randrange(35, 65) / 100.0
        satu = random.randrange(60, 95) / 100.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def update(self, sim, pos):
        if sim.peak_cell(pos, (0, 1)) is None:
            sim.move_particle(pos, (0, 1))
            return
        dirs = [1, -1]
        random.shuffle(dirs)
        for d in dirs:
            if sim.peak_cell(pos, (d, 1)) is None:
                sim.move_particle(pos, (d, 1))
                return
