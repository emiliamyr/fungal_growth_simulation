import pygame

def select_spore_location_and_conditions(engine, cell_size=20):
    """Allow the user to select the initial spore location and environmental conditions."""
    grid_size = engine.grid_size
    pygame.init()
    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size + 100))
    pygame.display.set_caption("Select spore location and environmental conditions")

    font = pygame.font.Font(None, 36)
    running = True
    selected_position = None
    temp = engine.T
    humidity = engine.H

    while running:
        screen.fill((0, 0, 0))

        for i in range(grid_size):
            for j in range(grid_size):
                if engine.grid[i, j] == -1:  # Barrier
                    pygame.draw.rect(screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size))
                else:
                    substrate_color = int(engine.substrate[i, j] * 255)
                    pygame.draw.rect(screen, (0, 0, substrate_color), (j * cell_size, i * cell_size, cell_size, cell_size))

        if selected_position:
            rect = pygame.Rect(
                selected_position[0] * cell_size,
                selected_position[1] * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)  # Green border for selected cell

        temp_text = font.render(f"Temperature (T): {temp}°C", True, (255, 255, 255))
        hum_text = font.render(f"Humidity (H): {humidity*100:.0f}%", True, (255, 255, 255))
        screen.blit(temp_text, (10, grid_size * cell_size + 10))
        screen.blit(hum_text, (10, grid_size * cell_size + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < grid_size * cell_size:
                    cell_x, cell_y = x // cell_size, y // cell_size
                    if 0 <= cell_x < grid_size and 0 <= cell_y < grid_size and engine.grid[cell_y, cell_x] != -1:
                        selected_position = (cell_x, cell_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_position:
                    running = False
                elif event.key == pygame.K_UP:
                    temp += 1
                elif event.key == pygame.K_DOWN:
                    temp -= 1
                elif event.key == pygame.K_RIGHT:
                    humidity = min(1.0, humidity + 0.05)
                elif event.key == pygame.K_LEFT:
                    humidity = max(0.0, humidity - 0.05)

    pygame.quit()
    return selected_position, temp, humidity
