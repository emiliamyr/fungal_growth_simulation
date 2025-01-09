import pygame
import numpy as np


def select_spore_location(engine, cell_size=20):
    """Allow the user to select the initial spore location on the generated substrate."""
    grid_size = engine.grid_size
    pygame.init()
    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
    pygame.display.set_caption("Select Spore Location")

    running = True
    selected_position = None

    while running:
        screen.fill((0, 0, 0))

        # Draw the substrate levels
        for i in range(grid_size):
            for j in range(grid_size):
                if engine.grid[i, j] == -1:  # Barrier
                    pygame.draw.rect(screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size))
                else:
                    substrate_color = int(engine.substrate[i, j] * 255)
                    pygame.draw.rect(screen, (0, 0, substrate_color), (j * cell_size, i * cell_size, cell_size, cell_size))

        # Highlight the selected cell
        if selected_position:
            rect = pygame.Rect(
                selected_position[0] * cell_size,
                selected_position[1] * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, (0, 255, 0), rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cell_x, cell_y = x // cell_size, y // cell_size
                # Ensure the selected position is not on a barrier
                if engine.grid[cell_y, cell_x] != -1:
                    selected_position = (cell_x, cell_y)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if selected_position:
                    running = False

    pygame.quit()
    return selected_position
