import pygame as pg
import numpy as np
import math

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
        
        for y in range(self.height - (2 * self.resolution), -1, -self.resolution):
            for x in range (0, self.width, self.resolution):
                current_cell = self.get_cell((x, y))
                if current_cell == 0:
                    continue
                bottom_cell = self.peak_cell((x, y), (0, 1))
                if bottom_cell == 0:
                    self.place_cell((x, y), 0)
                    self.place_cell((x, y+self.resolution), 1)
                

    
    def draw(self):
        if self.is_dirty:
            self.screen.fill("black")
            self.draw_grid()
            self.draw_cells()
            self.is_dirty = False

    def clear(self):
        self.cells = np.zeros(self.convert_coordinate_to_grid((self.width, self.height)))
        self.is_dirty = True
        
    def get_mouse_cell_pos(self):
        return (
            math.floor(self.global_mouse_pos[0] / self.resolution),
            math.floor(self.global_mouse_pos[1] / self.resolution)
        )

    def peak_cell(self, pos, dir):
        pos = self.convert_coordinate_to_grid(pos)
        p = (pos[0] + dir[0], pos[1] + dir[1])
        return self.cells[p[0], p[1]]

    def get_cell(self, pos):
        p = self.convert_coordinate_to_grid(pos)
        return self.cells[p[0], p[1]]

    def place_cell(self, pos, val = 1):
        pos = self.convert_coordinate_to_grid(pos)
        self.cells[pos[0], pos[1]] = val
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
        if pg.mouse.get_pressed()[0]:
            self.place_cell(self.global_mouse_pos)
        if pg.mouse.get_pressed()[1]:
            self.place_cell(self.global_mouse_pos, 0)
    
    def convert_coordinate_to_grid(self, pos):
        return (math.floor(pos[0] / self.resolution), math.floor(pos[1] / self.resolution))

    def draw_grid(self):
        for x in range(0, self.width, self.resolution):
            pg.draw.line(self.screen, "grey50", (x, 0), (x, self.height))
        for y in range(0, self.height, self.resolution):
            pg.draw.line(self.screen, "grey50", (0, y), (self.width, y))

    def draw_cells(self):
        for y in range(0, self.height, self.resolution):
            for x in range(0, self.width, self.resolution):
                current_cell = self.cells[self.convert_coordinate_to_grid((x, y))]
                if current_cell != 0:
                    rect = pg.Rect(x, y, self.resolution, self.resolution)
                    pg.draw.rect(self.screen, "white", rect)
