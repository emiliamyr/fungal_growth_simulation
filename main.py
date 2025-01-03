from growth_engine import GrowthEngine
from spore_selector import select_spore_location
import random
import pygame
import numpy as np


def main():
    grid_size = 50
    steps = 100
    T = 25
    H = 0.8
    barrier_size = 10
    scale = 10

    initial_spore = select_spore_location(grid_size)
    if not initial_spore:
        print("No spore location selected. Exiting.")
        return

    engine = GrowthEngine(grid_size, T, H, steps)
    engine.fungal_density[initial_spore[1], initial_spore[0]] = 1.0

    for _ in range(5):
        x, y = random.randint(0, grid_size - barrier_size), random.randint(0, grid_size - barrier_size)
        engine.add_barrier(x, y, size=barrier_size)

    # engine.simulate(steps)
    display_simulation(engine, steps, scale)


def display_simulation(engine, steps, scale):
    pygame.init()

    height, width = engine.fungal_density.shape
    width, height = width * scale, height * scale
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Symulacja Grzybni")

    clock = pygame.time.Clock()
    running = True

    for step in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if not running:
            break

        engine.update_growth()

        if step % 10 == 0:
            fungal_density = engine.fungal_density
            if np.max(fungal_density) > 0:
                fungal_surface = (255 * fungal_density / np.max(fungal_density)).astype(np.uint8)
            else:
                fungal_surface = np.zeros_like(fungal_density)

            fungal_surface = np.stack([np.zeros_like(fungal_surface), fungal_surface, np.zeros_like(fungal_surface)],
                                      axis=-1)

            nutrients = engine.nutrients
            if np.max(nutrients) > 0:
                nutrient_surface = (255 * nutrients / np.max(nutrients)).astype(np.uint8)
            else:
                nutrient_surface = np.zeros_like(nutrients)

            nutrient_surface = np.stack(
                [np.zeros_like(nutrient_surface), np.zeros_like(nutrient_surface), nutrient_surface], axis=-1)

            combined_surface = fungal_surface + nutrient_surface

            pygame_surface = pygame.surfarray.make_surface(np.transpose(combined_surface, (1, 0, 2)))

            screen.blit(pygame.transform.scale(pygame_surface, (width, height)), (0, 0))
            pygame.display.flip()

        clock.tick(30)
    GrowthEngine.render(engine, steps)
    pygame.quit()


if __name__ == "__main__":
    main()
