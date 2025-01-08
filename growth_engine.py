import matplotlib.pyplot as plt
import numpy as np
from barrier import Barrier


class GrowthEngine:
    def __init__(self, grid_size, T, H, steps):
        self.grid_size = grid_size
        self.fungal_density = np.zeros((grid_size, grid_size))
        self.nutrients = np.random.rand(grid_size, grid_size)
        self.T = int(T)
        self.H = float(H)
        self.D = 0.5
        self.K = 1.0
        self.D_nutrients = 0.05
        self.barriers = []
        self.steps = steps
        self.cellular_automata_grid = np.zeros((grid_size, grid_size), dtype=bool)

    def add_barrier(self, x, y, size):
        barrier = Barrier(x, y, size)
        self.barriers.append(barrier)

    def add_spore(self, x, y):
        """Dodaj zarodnik na siatce."""
        self.fungal_density[y, x] = 1.0

    def laplacian(self, array):
        laplace = (
                np.roll(array, 1, axis=0) + np.roll(array, -1, axis=0) +
                np.roll(array, 1, axis=1) + np.roll(array, -1, axis=1) -
                4 * array
        )

        laplace[0, :] = 0
        laplace[-1, :] = 0
        laplace[:, 0] = 0
        laplace[:, -1] = 0
        return laplace

    def update_nutrients(self):
        laplace = self.laplacian(self.nutrients)
        diffusion_rate = self.D_nutrients
        self.nutrients += diffusion_rate * laplace
        self.nutrients = np.maximum(self.nutrients, 0)

    def update_fungal_density(self):
        new_density = np.copy(self.fungal_density)
        for i in range(1, self.grid_size - 1):
            for j in range(1, self.grid_size - 1):
                if self.fungal_density[i, j] == 0:
                    neighbors = np.sum(self.fungal_density[i - 1:i + 2, j - 1:j + 2]) - self.fungal_density[i, j]
                    if neighbors > 0 and self.nutrients[i, j] > 0.1:
                        new_density[i, j] = 1
                elif self.fungal_density[i, j] == 1:
                    if self.nutrients[i, j] <= 0:
                        new_density[i, j] = 0
                    else:
                        self.nutrients[i, j] -= 0.05
        self.fungal_density = new_density

    def update_cellular_automata(self):
        new_automata_grid = np.copy(self.cellular_automata_grid)

        for i in range(1, self.grid_size - 1):
            for j in range(1, self. grid_size - 1):
                if not self.cellular_automata_grid[i, j]:
                    neighbors = [
                        (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                        (i, j - 1), (i, j + 1),
                        (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
                    ]
                    active_neighbors = sum(
                        self.cellular_automata_grid[ni, nj]
                        for ni, nj in neighbors
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size
                    )
                    if active_neighbors > 0 and self.nutrients[i, j] > 0.1:
                        new_automata_grid[i, j] = True
                        if self.cellular_automata_grid[i, j]:
                            self.fungal_density[i, j] = max(self.fungal_density[i, j], 0.1)  # Minimalna wartość wzrostu
                else:
                    if self.nutrients[i, j] < 0.05:
                        new_automata_grid[i, j] = False

        self.cellular_automata_grid = new_automata_grid

    def update_growth(self):
        dx = 0.8
        dt = 0.1

        laplace = self.laplacian(self.fungal_density) / dx**2

        growth = self.r() * self.fungal_density * (1 - self.fungal_density / self.K)
        growth[self.fungal_density >= self.K] = 0

        self.fungal_density += dt * (self.D * laplace + growth)

        self.nutrients -= growth * 0.05

        for barrier in self.barriers:
            for i in range(barrier.rect.top, barrier.rect.bottom):
                for j in range(barrier.rect.left, barrier.rect.right):
                    self.fungal_density[i, j] = 0
                    self.nutrients[i, j] = 0

        self.fungal_density = np.maximum(self.fungal_density, 0)
        self.nutrients[self.fungal_density > 0.1] = np.minimum(
            self.nutrients[self.fungal_density > 0.1], 0.1
        )
        self.nutrients = np.maximum(self.nutrients, 0)

        self.update_cellular_automata()

        self.fungal_density[self.cellular_automata_grid] = np.minimum(
            self.fungal_density[self.cellular_automata_grid], self.K
        )

    def render(self, step):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        ax1, ax2 = axes
        im1 = ax1.imshow(self.fungal_density, cmap="Greens", interpolation="nearest")
        ax1.set_title(f"Fungal Density (Step {step})")
        plt.colorbar(im1, ax=ax1)
        im2 = ax2.imshow(self.nutrients, cmap="Blues", interpolation="nearest")
        ax2.set_title(f"Nutrient Levels (Step {step})")
        plt.colorbar(im2, ax=ax2)
        plt.savefig(f"output_step_{step}.png")
        plt.close()

    def simulate(self, steps):
        for step in range(steps):
            self.update_growth()
            #if step % 10 == 0:
                #self.render(step)

    def r(self):
        Topt, σT = 25, 5
        Hopt = 0.8
        KN = 0.5
        r_max = 0.1
        """Funkcja wzrostu zależna od temperatury, wilgotności i lokalnych składników odżywczych."""
        fT = np.exp(-((self.T - Topt) ** 2) / (2 * σT ** 2))
        fH = self.H / Hopt if self.H <= Hopt else (2 - self.H / Hopt)
        fN = self.nutrients / (KN + self.nutrients)
        return r_max * fT * fH * fN
