import pygame as pg
from simulation import Simulation

def main():
    pg.init()

    simulation = Simulation(800, 600, 10)
    simulation.loop()
    pg.quit()

if __name__ == "__main__":
    main()
