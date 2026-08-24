from particle import Particle
import random
import colorsys

class Stone(Particle):
    def __init__(self):
        self.is_solid = True
        hue = 0.0
        light = random.randrange(14, 50) / 100.0
        satu = 0.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def update(self, sim, pos):
        pass
