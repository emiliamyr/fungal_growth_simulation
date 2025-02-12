import numpy as np
import pygame
from barrier import Barrier
import random

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

class GrowthEngine:
    def __init__(self, grid_size, T, H, steps):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=np.float32)
        self.substrate = np.clip(
            np.random.normal(loc=0.2, scale=0.1, size=(grid_size, grid_size)), 0.0, 1.0
        )
        self.age = np.zeros((grid_size, grid_size), dtype=np.float32)
        self.tips = []
        self.T = T
        self.H = H
        self.steps = steps
        self.barriers = []

    def calculate_occupied_area_percentage(self):
        """Oblicza procent powierzchni zajętej przez grzybnię."""
        occupied_cells = np.sum(self.grid > 0)
        total_cells = self.grid_size * self.grid_size
        return (occupied_cells / total_cells) * 100

    def add_barrier(self, x, y, size):
        barrier = Barrier(x, y, size)
        self.barriers.append(barrier)
        for i in range(barrier.rect.top, barrier.rect.bottom):
            for j in range(barrier.rect.left, barrier.rect.right):
                if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
                    self.grid[i, j] = -1

    def add_spore(self, x, y):
        self.tips.append((x, y))
        self.grid[y, x] = 0.1

    def initialize_circular_tips(self, center_x, center_y, num_tips=10):
        """Initialize fungal tips in a circular pattern around the center with outward directions."""
        for i in range(num_tips):
            angle = 2 * np.pi * i / num_tips
            dx = int(round(np.cos(angle)))
            dy = int(round(np.sin(angle)))
            tip_x, tip_y = center_x + dx, center_y + dy
            if 0 <= tip_x < self.grid_size and 0 <= tip_y < self.grid_size:
                self.add_spore(tip_x, tip_y)
                self.age[tip_y, tip_x] = 0

    def growth_rate(self, T, H, N):
        T_OPT, SIGMA_T = 25, 5
        H_OPT = 0.8
        K_N = 0.5
        R_MAX = 1.0

        f_T = np.exp(-((T - T_OPT) ** 2) / (2 * SIGMA_T ** 2))
        f_H = min(H / H_OPT, 1.0)
        f_N = N / (K_N + N)

        return R_MAX * f_T * f_H * f_N

    def update_substrate(self):
        laplace = (
                np.roll(self.substrate, 1, axis=0) + np.roll(self.substrate, -1, axis=0) +
                np.roll(self.substrate, 1, axis=1) + np.roll(self.substrate, -1, axis=1) -
                4 * self.substrate
        )

        self.substrate += 0.001 * (0.1 * laplace)
        self.substrate -= self.grid * 0.01
        self.substrate = np.clip(self.substrate, 0, 1)

    def simulate_one_step(self):
        """Symulacja jednego kroku wzrostu grzybni."""
        new_tips = []
        for x, y in self.tips:
            if self.age[y, x] > 15:
                for _ in range(random.randint(2, 4)):
                    best_directions = sorted(
                        DIRECTIONS,
                        key=lambda d: self.substrate[y + d[1], x + d[0]]
                        if 0 <= y + d[1] < self.grid_size and 0 <= x + d[0] < self.grid_size else -1,
                        reverse=True
                    )
                    for dx, dy in best_directions:
                        branch_x, branch_y = x + dx, y + dy
                        if 0 <= branch_x < self.grid_size and 0 <= branch_y < self.grid_size:
                            if self.grid[branch_y, branch_x] == 0 and self.substrate[branch_y, branch_x] > 0.1:
                                self.grid[branch_y, branch_x] = 0.1
                                self.substrate[branch_y, branch_x] -= 0.01
                                self.age[branch_y, branch_x] = 0
                                new_tips.append((branch_x, branch_y))
                                break
                continue

            if random.random() < 0.002:
                continue

            local_growth_rate = self.growth_rate(self.T, self.H, self.substrate[y, x])
            biomass_growth = local_growth_rate * 0.0005

            if self.grid[y, x] + biomass_growth > 1.0:
                continue

            best_directions = sorted(
                DIRECTIONS,
                key=lambda d: self.substrate[y + d[1], x + d[0]]
                if 0 <= y + d[1] < self.grid_size and 0 <= x + d[0] < self.grid_size else -1,
                reverse=True
            )

            for dx, dy in best_directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.grid[ny, nx] == 0 and self.substrate[ny, nx] > 0.1:
                        self.grid[ny, nx] += biomass_growth
                        self.substrate[ny, nx] -= 0.01
                        self.age[ny, nx] = self.age[y, x] + 1
                        new_tips.append((nx, ny))
                        break

        self.tips = new_tips

    def visualize(self, screen, scale):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] > 0:
                    normalized_age = self.age[i, j] / np.max(self.age[self.grid > 0]) if np.max(self.age) > 0 else 0
                    red = int(255 * normalized_age)
                    green = int(255 * (1 - normalized_age))
                    pygame.draw.rect(screen, (red, green, 0), (j * scale, i * scale, scale, scale))
                elif self.grid[i, j] == -1:  # Barriers
                    pygame.draw.rect(screen, (0, 0, 0), (j * scale, i * scale, scale, scale))
                else:
                    substrate_color = int(self.substrate[i, j] * 255)
                    pygame.draw.rect(screen, (0, 0, substrate_color), (j * scale, i * scale, scale, scale))
