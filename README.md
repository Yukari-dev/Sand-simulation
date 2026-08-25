# Falling Sand Simulation

A 2D falling-sand simulation written in Python using Pygame and NumPy. The engine implements grid-based cellular automata to simulate granular materials, fluids, and reactive elements in real time.
Overview

The project models particle interactions on a two-dimensional grid. Each cell updates based on its element properties such as density, state of matter, and combustion rules allowing complex emergent behaviors to arise from simple localized update logic.
Supported Elements

    Sand: Heavy granular material that falls downward and slides diagonally off obstacles.
    Water: Liquid that falls downward and disperses horizontally across available space.
    Stone: Static solid material acting as an immovable barrier.
    Wood: Flammable solid structure act as fuel for the fire.
    Fire: Volatile element that consumes adjacent flammable elements before dissipating.
    Smoke: Get instantiated after `Fire` element dissipate.

## Requirements
    Python 3.10+
    Pygame 2.5+
    NumPy

## Installation
    Clone the repository:
    git clone https://github.com/your-username/Sand-simulation.git
    cd Sand-simulation

    Set up a virtual environment:
    python -m venv .env
    source .env/bin/activate  # On Windows use: .env\Scripts\activate

    Install the required dependencies:
    pip install pygame numpy

## Usage

Run the main application entry point:
python main.py
Controls

    Draw Element: Left Mouse Click / Drag
    Erase Cell: Right Mouse Click / Drag
    Change Brush Size: Mouse Scroll Wheel
    Select Eraser: Key 1
    Select Sand: Key 2
    Select Stone: Key 3
    Select Water: Key 4
    Select Wood: Key 5
    Select Fire: Key 6
    Reset Grid: Key R
    Exit: Key Q or ESC

## Project Structure
    main.py: Application entry point and loop setup
    simulation.py: Core Simulation class, grid operations, and rendering logic
    particles/elements.py: Base particle class and individual element implementations
## License
Feel free to do anything with it!! (I use cachyOS btw ^W^)
