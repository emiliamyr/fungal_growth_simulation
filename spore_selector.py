import pygame
import numpy as np


def select_spore_location(grid_size, cell_size=20):
    """Allow the user to select the initial spore location using pygame."""
    pygame.init()
    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
    pygame.display.set_caption("Select Spore Location")

    running = True
    selected_position = None

    while running:
        screen.fill((255, 255, 255))

        for x in range(0, grid_size * cell_size, cell_size):
            for y in range(0, grid_size * cell_size, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

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
                selected_position = (x // cell_size, y // cell_size)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if selected_position:
                    running = False

    pygame.quit()
    return selected_position
