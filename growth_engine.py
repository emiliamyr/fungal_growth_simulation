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
        self.D = 1.5
        self.K = 1.0
        self.barriers = []
        self.steps = steps

    def add_barrier(self, x, y, size):
        """Dodaj przeszkodę na siatce."""
        barrier = Barrier(x, y, size)
        self.barriers.append(barrier)

    def add_spore(self, x, y):
        """Dodaj zarodnik na siatce."""
        self.fungal_density[y, x] = 1.0

    def laplacian(self):
        laplace = (
                np.roll(self.fungal_density, 1, axis=0) + np.roll(self.fungal_density, -1, axis=0) +
                np.roll(self.fungal_density, 1, axis=1) + np.roll(self.fungal_density, -1, axis=1) -
                4 * self.fungal_density
        )

        laplace[0, :] = 0
        laplace[-1, :] = 0
        laplace[:, 0] = 0
        laplace[:, -1] = 0
        return laplace

    def update_growth(self):
        dx = 1.0
        dt = 0.05

        laplace = self.laplacian() / dx**2

        growth = self.r() * self.fungal_density * (1 - self.fungal_density / self.K)
        growth[self.fungal_density >= self.K * 0.9] = 0

        self.fungal_density += dt * (self.D * laplace + growth)

        self.nutrients -= growth * 0.05
        self.nutrients = np.maximum(self.nutrients, 0)

        for barrier in self.barriers:
            for i in range(barrier.rect.top, barrier.rect.bottom):
                for j in range(barrier.rect.left, barrier.rect.right):
                    self.fungal_density[i, j] = 0
                    self.nutrients[i, j] = 0

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
