from growth_engine import GrowthEngine
from spore_selector import select_spore_location
import random
import pygame


def main():
    grid_size = 100
    steps = 100000
    T = 25
    H = 0.8
    barrier_size = 10
    scale = 10
    num_tips = 10  # Number of initial tips

    # Initialize the growth engine
    engine = GrowthEngine(grid_size, T, H, steps)

    # Add barriers
    for _ in range(3):  # Number of barriers
        x, y = random.randint(0, grid_size - barrier_size), random.randint(0, grid_size - barrier_size)
        engine.add_barrier(x, y, barrier_size)

    # Allow the user to select the center for fungal growth
    spore_location = select_spore_location(engine, cell_size=scale)
    if spore_location is None:
        print("No spore location selected. Exiting.")
        return

    # Initialize the fungal growth at the selected center
    engine.initialize_circular_tips(spore_location[0], spore_location[1], num_tips)

    # Start the simulation display
    display_simulation(engine, steps, scale)



def display_simulation(engine, steps, scale):
    pygame.init()

    screen = pygame.display.set_mode((engine.grid_size * scale, engine.grid_size * scale))
    pygame.display.set_caption("Enhanced Fungal Growth Simulation with Barriers")

    clock = pygame.time.Clock()
    running = True

    for step in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        engine.simulate()
        engine.update_substrate()

        screen.fill((0, 0, 0))
        engine.visualize(screen, scale)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
