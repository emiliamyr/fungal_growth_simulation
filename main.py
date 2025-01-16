from growth_engine import GrowthEngine
from spore_selector import select_spore_location_and_conditions
import random
import pygame
import csv

def main():
    grid_size = 70
    steps = 100
    T = 25
    H = 0.8
    barrier_size = 10
    scale = 10
    num_tips = 10
    results = []

    engine = GrowthEngine(grid_size, T, H, steps)

    for _ in range(0):
        x, y = random.randint(0, grid_size - barrier_size), random.randint(0, grid_size - barrier_size)
        engine.add_barrier(x, y, barrier_size)

    spore_location, T, H = select_spore_location_and_conditions(engine, cell_size=scale)
    if spore_location is None:
        print("No spore location selected. Exiting.")
        return

    engine.T = T
    engine.H = H
    engine.initialize_circular_tips(spore_location[0], spore_location[1], num_tips)
    output_file = f"fungal_growth_results_{T}_{H}.csv"

    display_simulation(engine, steps, scale, output_file)

def save_to_file(filename, data):
    """Zapisuje dane do pliku CSV."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Occupied Area (%)"])  # Nagłówki
        writer.writerows(data)

def display_simulation(engine, steps, scale, output_file):
    pygame.init()

    screen = pygame.display.set_mode((engine.grid_size * scale, engine.grid_size * scale))
    pygame.display.set_caption("Enhanced Fungal Growth Simulation with Barriers")

    clock = pygame.time.Clock()
    running = True
    results = []
    for step in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        engine.simulate_one_step()
        engine.update_substrate()

        occupied_area = engine.calculate_occupied_area_percentage()
        results.append([step, occupied_area])

        screen.fill((0, 0, 0))
        engine.visualize(screen, scale)
        pygame.display.flip()

        clock.tick(6)

    save_to_file(output_file, results)
    pygame.quit()


if __name__ == "__main__":
    main()
