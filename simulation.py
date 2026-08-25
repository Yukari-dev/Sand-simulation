import pygame as pg
import numpy as np
from particles.elements import Sand, Stone, Water, Wood, Fire
import math
import random


class Simulation:
    def __init__(self, width, height, resolution):
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.width = width
        self.height = height
        self.resolution = resolution
        self.running = True
        self.dt = 0
        self.is_dirty = False
        self.current_particle = Sand
        self.brush_size = 1
        self.clear()

    def loop(self):
        self.draw_grid()
        while self.running:
            self.event()
            self.update()
            self.draw()
            self.refresh()

    def refresh(self):
        pg.display.flip()
        self.dt = self.clock.tick(60) / 1000

    def update(self):
        self.global_mouse_pos = pg.mouse.get_pos()
        width, height = self.cells.shape
        for x in range(width):
            for y in range(height):
                cell = self.cells[x, y]
                if cell is not None:
                    cell.updated = False

        for y in range(self.height - (2 * self.resolution),
                       -1, -self.resolution):
            x_coord = list(range(0, self.width, self.resolution))
            random.shuffle(x_coord)

            for x in x_coord:
                cell = self.get_cell((x, y))
                if cell is not None and not cell.updated:
                    cell.updated = True
                    cell.update(self, (x, y))

    def draw(self):
        if self.is_dirty:
            self.screen.fill("black")
            # self.draw_grid()
            self.draw_cells()
            self.is_dirty = False
        self.draw_hud()

    def clear(self):
        size = self.convert_coordinate_to_grid((self.width, self.height))
        self.cells = np.full(size, None)
        self.is_dirty = True

    def get_mouse_cell_pos(self):
        return (
            math.floor(self.global_mouse_pos[0] / self.resolution),
            math.floor(self.global_mouse_pos[1] / self.resolution)
        )

    def is_inside(self, pos, dir):
        grid_pos = self.convert_coordinate_to_grid(pos)
        nx = grid_pos[0] + dir[0]
        ny = grid_pos[1] + dir[1]

        total_width, total_height = self.cells.shape

        if nx < 0 or nx >= total_width or ny < 0 or ny >= total_height:
            return False
        return True

    def is_empty(self, pos, dir):
        grid_pos = self.convert_coordinate_to_grid(pos)
        nx = grid_pos[0] + dir[0]
        ny = grid_pos[1] + dir[1]

        total_width, total_height = self.cells.shape

        if nx < 0 or nx >= total_width or ny < 0 or ny >= total_height:
            return False
        return self.cells[nx, ny] is None

    def peek_cell(self, pos, dir):
        if not self.is_inside(pos, dir):
            return None
        gpos = self.convert_coordinate_to_grid(pos)
        nx, ny = gpos[0] + dir[0], gpos[1] + dir[1]
        return self.cells[nx, ny]

    def get_cell(self, pos):
        p = self.convert_coordinate_to_grid(pos)
        return self.cells[p[0], p[1]]

    def place_cell(self, pos, particle):
        p = self.convert_coordinate_to_grid(pos)
        if 0 <= p[0] < self.cells.shape[0] and 0 <= p[1] < self.cells.shape[1]:
            self.cells[p[0], p[1]] = particle() if particle else None
            self.is_dirty = True

    def place_brush(self, pos, element):
        radius = getattr(self, "brush_size", 1) - 1
        gx, gy = self.convert_coordinate_to_grid(pos)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx+dy*dy <= radius*radius + 0.5:
                    px = (gx + dx) * self.resolution
                    py = (gy + dy) * self.resolution
                    self.place_cell((px, py), element)

    def move_particle(self, pos, dir):
        if not self.is_inside(pos, dir):
            return
        gpos = self.convert_coordinate_to_grid(pos)
        nx, ny = gpos[0] + dir[0], gpos[1] + dir[1]

        self.cells[nx, ny] = self.cells[gpos[0], gpos[1]]
        self.cells[gpos[0], gpos[1]] = None
        self.is_dirty = True

    def swap_particles(self, pos1, pos2):
        g1 = self.convert_coordinate_to_grid(pos1)
        g2 = self.convert_coordinate_to_grid(pos2)

        self.cells[g1[0], g1[1]], self.cells[g2[0], g2[1]] = (
            self.cells[g2[0], g2[1]], self.cells[g1[0], g1[1]]
        )
        self.is_dirty = True

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_r:
                    self.clear()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:   self.current_particle = None
                if event.key == pg.K_2:   self.current_particle = Sand
                elif event.key == pg.K_3: self.current_particle = Stone
                elif event.key == pg.K_4: self.current_particle = Water
                elif event.key == pg.K_5: self.current_particle = Wood
                elif event.key == pg.K_6:self.current_particle = Fire
            if event.type == pg.MOUSEWHEEL:
                if not hasattr(self, "brush_size"): self.brush_size = 1
                self.brush_size = max(1, min(8, self.brush_size + event.y))
        if pg.mouse.get_pressed()[0]:
            self.place_brush(self.global_mouse_pos, self.current_particle)
        if pg.mouse.get_pressed()[2]:
            self.place_brush(self.global_mouse_pos, None)

    def convert_coordinate_to_grid(self, pos):
        return (
            math.floor(pos[0] / self.resolution),
            math.floor(pos[1] / self.resolution)
        )

    def draw_grid(self):
        for x in range(0, self.width, self.resolution):
            pg.draw.line(self.screen, "grey50", (x, 0), (x, self.height))
        for y in range(0, self.height, self.resolution):
            pg.draw.line(self.screen, "grey50", (0, y), (self.width, y))

    def draw_cells(self):
        for y in range(0, self.height, self.resolution):
            for x in range(0, self.width, self.resolution):
                current_cell = self.cells[
                    self.convert_coordinate_to_grid((x, y))
                ]
                if current_cell is not None:
                    rect = pg.Rect(x, y, self.resolution, self.resolution)
                    pg.draw.rect(self.screen, current_cell.color, rect)

    def draw_hud(self):
        if not hasattr(self, 'font'):
            pg.font.init()
            self.font = pg.font.SysFont("jetbrainsmononerdfontmono", 14, bold=True)
        active_count = np.count_nonzero(self.cells != None)
        fps = int(self.clock.get_fps())
        elem_name = self.current_particle.__name__ if self.current_particle else "Eraser"
        brush_size = self.brush_size

        hud_str = f"FPS: {fps} | Particles: {active_count} | Element: {elem_name} | Brush: {brush_size}"
        surface = self.font.render(hud_str, True, (255, 255, 255))

        bg_rect = pg.Rect(10, 10, surface.get_width() + 16, 26)
        pg.draw.rect(self.screen, (20, 20, 20), bg_rect)
        pg.draw.rect(self.screen, (70, 70, 70), bg_rect, 1)
        self.screen.blit(surface, (18, 15))
