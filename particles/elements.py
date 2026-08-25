import random
import colorsys
from particles.base import MovableSolid, StaticSolid, Liquid, Gas


class Sand(MovableSolid):
    def __init__(self):
        super().__init__()
        hue = random.uniform(0.08, 0.13)
        light = random.uniform(0.35, 0.65)
        satu = random.uniform(0.60, 0.95)
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def update(self, sim, pos):
        if sim.is_inside(pos, (0, 1)):
            target_down = sim.peek_cell(pos, (0, 1))
            if isinstance(target_down, Liquid):
                sim.swap_particles(pos, (pos[0], pos[1] + sim.resolution))
                return
        super().update(sim, pos)


class Stone(StaticSolid):
    def __init__(self):
        hue = 0.0
        light = random.randrange(14, 50) / 100.0
        satu = 0.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


class Wood(StaticSolid):
    flammable = True

    def __init__(self):
        super().__init__()
        hue = 0.075
        light = random.uniform(0.20, 0.72)
        satu = random.uniform(0.50, 0.90)
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


class Water(Liquid):
    viscosity = 1.0

    def __init__(self):
        super().__init__()
        hue = random.randrange(181, 217) / 360.0
        light = 50.0 / 100.0
        satu = random.randrange(50, 100) / 100.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


class Smoke(Gas):
    def __init__(self):
        super().__init__()
        hue = 0.0
        # Use uniform for float ranges!
        light = random.uniform(0.21, 0.65)
        satu = 0.0
        rgb = colorsys.hls_to_rgb(hue, light, satu)
        self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


class Fire(Gas):
    def __init__(self):
        super().__init__()
        self.life = random.randint(15, 30)
        self.color = (255, random.randint(80, 160), 0)

    def update(self, sim, pos):
        self.life -= 1
        if self.life <= 0:
            sim.place_cell(pos, Smoke if random.random() < 0.3 else None)
            return
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for d in dirs:
            neighbor = sim.peek_cell(pos, d)
            if neighbor and getattr(neighbor, "flammable", False):
                px = pos[0] + d[0] * sim.resolution
                py = pos[1] + d[1] * sim.resolution
                sim.place_cell((px, py), Fire)
        super().update(sim, pos)
