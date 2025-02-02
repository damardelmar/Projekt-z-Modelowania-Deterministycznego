import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Apartment:
    """
    This class is an apartment that holds information about its walls, windows and heaters.
    """
    def __init__(self, width, height, T, f0, power, avg_temp_lim=20, avg_temp_outside=0):
        """
        Creates an apartment with the following attributes
        :param width: Width of apartment
        :param height: Height of apartment
        :param T: Duration of the Simulation
        :param f0: Function that defines the initial heat state in the apartment
        :param power: The power of all heaters (in Watts)
        :param avg_temp_lim: Maximum average temperature in room before heaters turn off
        :param avg_temp_outside: Temperature outside that will decide how much windows will cool the room
        """
        self.T = T * 60
        self.h_x = 0.1
        self.h_t = 0.0049
        self.t = np.arange(0, self.T, self.h_t)
        x = np.arange(0, width + self.h_x, self.h_x)
        y = np.arange(0, height + self.h_x, self.h_x)
        self.X, self.Y = np.meshgrid(x, y)
        self.u = np.zeros([len(self.t), len(y), len(x)])
        self.u[0, :, :] = f0(self.X, self.Y)
        self.power = power
        self.avg_temp_lim = 273.15 + avg_temp_lim
        self.avg_temp_outside = 273.15 + avg_temp_outside
        self.energy_usage = 0

        self.x_walls = []
        self.y_walls = []
        self.heaters = []
        self.x_windows = []
        self.y_windows = []

    def add_x_wall(self, x1, x2, y):
        """
        Adds dimensions of a horizontal wall
        """
        self.x_walls.append((x1, x2, y))

    def add_y_wall(self, x, y1, y2):
        """
        Add dimensions of a vertical wall
        """
        self.y_walls.append((x, y1, y2))

    def add_x_window(self, x1, x2, y):
        """
        Adds dimensions of a horizontal window
        """
        self.x_windows.append((x1, x2, y))

    def add_y_window(self, x, y1, y2):
        """
        Adds dimensions of a vertical window
        """
        self.y_windows.append((x, y1, y2))

    def add_heater(self, x1, x2, y1, y2, rx1, rx2, ry1, ry2):
        """
        Adds a heater with its dimensions and the dimensions of the room it's heating
        """
        self.heaters.append((x1, x2, y1, y2, rx1, rx2, ry1, ry2))


class Visualiser:
    """
    This class serves to visualise everything that the Apartment class represents
    """
    def __init__(self, apartment):
        """
        Connects to apartment
        """
        self.apartment = apartment

    def draw(self):
        """
        Draws the apartment with its walls, windows, and heaters
        """
        plt.fill_between([self.apartment.X[0, 0], self.apartment.X[0, -1]], self.apartment.Y[0, 0], self.apartment.Y[-1, -1], color='#edbd79', alpha=0.5,
                         label="Filled Rectangle")

        plt.plot([self.apartment.X[0, 0], self.apartment.X[0, -1]],
                 [self.apartment.Y[0, 0], self.apartment.Y[0, 0]], label="Line", color='black')

        plt.plot([self.apartment.X[0, 0], self.apartment.X[0, -1]],
                 [self.apartment.Y[-1, -1], self.apartment.Y[-1, -1]], label="Line", color='black')

        plt.plot([self.apartment.X[0, 0], self.apartment.X[0, 0]],
                 [self.apartment.Y[0, 0], self.apartment.Y[-1, -1]], label="Line", color='black')

        plt.plot([self.apartment.X[0, -1], self.apartment.X[0, -1]],
                 [self.apartment.Y[0, 0], self.apartment.Y[-1, -1]], label="Line", color='black')

        for x1, x2, y1, y2, rx1, rx2, ry1, ry2 in self.apartment.heaters:
            plt.fill_between([x1, x2], y1, y2, color='red', alpha=0.5,
                             label="Filled Rectangle")

        for x1, x2, y in self.apartment.x_walls:
            plt.plot([x1, x2], [y, y], label="Line", color='black')

        for x, y1, y2 in self.apartment.y_walls:
            plt.plot([x, x], [y1, y2], label="Line", color='black')

        for x1, x2, y in self.apartment.x_windows:
            plt.plot([x1, x2], [y, y], label="Line", color='#a3daff')

        for x, y1, y2 in self.apartment.y_windows:
            plt.plot([x, x], [y1, y2], label="Line", color='#a3daff')

        plt.show()

    def plot_heatmap(self, percent):
        """
        Plots the heatmap of the solution
        :param percent: Determines what percentage of time that has elapsed since the start of the simulation.
        """
        index = min(int(self.apartment.u.shape[0] * percent), self.apartment.u.shape[0] - 1)
        plt.pcolormesh(self.apartment.X, self.apartment.Y, self.apartment.u[index, :, :] - 273.15, shading='auto')
        plt.colorbar(label="Temperature [C]")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        if percent == 1:
            plt.title(f"Heat Dispersion \n t = {round(index * self.apartment.h_t / 60, 2)} min \n Gross Energy Usage = {round(self.apartment.energy_usage, 2)}J")
        else:
            plt.title(
                f"Heat Dispersion \n t = {round(index * self.apartment.h_t / 60, 2)} min")
        plt.show()

    def animate_solution(self):
        """
        Makes an animation of the solution
        """
        fig, ax = plt.subplots(figsize=(20, 5))

        u1 = self.apartment.u[::500, :, :] - 273.15
        mesh = ax.pcolormesh(self.apartment.X, self.apartment.Y, u1[-1, :, :])
        fig.colorbar(mesh, ax=ax, label="Temperature [C]")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Heat Dispersion Animation \n t = 0 min")

        def update(frame):
            mesh.set_array(u1[frame, :, :].ravel())
            ax.set_title(f"Heat Dispersion Animation \n t = {round(frame * 500 * self.apartment.h_t / 60, 2)} min")
            return mesh,

        anim = FuncAnimation(fig, update, frames=u1.shape[0], interval=5)

        plt.show()


class Solver:
    """
    This class solves the heat equations for the apartment and saves them
    """
    def __init__(self, apartment):
        self.apartment = apartment

    def x_indexer(self, x):
        """
        Returns the respective index in the solution array for the inputted x coordinate
        """
        return np.max(np.where(self.apartment.X[0, :] <= x)[0])

    def y_indexer(self, y):
        """
        Returns the respective index in the solution array for the inputted y coordinate
        """
        return np.max(np.where(self.apartment.Y[:, 0] <= y)[0])

    def solve(self):
        """
        Solves the heat equation by taking into account walls, windows and heaters.
        """
        for x1, x2, y in self.apartment.x_windows:
            x1 = self.x_indexer(x1)
            x2 = self.x_indexer(x2)
            y = self.y_indexer(y)
            self.apartment.u[0, y, x1: x2 + 1] = self.apartment.avg_temp_outside

        for x, y1, y2 in self.apartment.y_windows:
            x = self.x_indexer(x)
            y1 = self.y_indexer(y1)
            y2 = self.y_indexer(y2)
            self.apartment.u[0, y1: y2 + 1, x] = self.apartment.avg_temp_outside

        for x1, x2, y in self.apartment.x_walls:
            x1 = self.x_indexer(x1)
            x2 = self.x_indexer(x2)
            y = self.y_indexer(y)
            self.apartment.u[0, y, x1: x2 + 1] = 273.15

        for x, y1, y2 in self.apartment.y_walls:
            x = self.x_indexer(x)
            y1 = self.y_indexer(y1)
            y2 = self.y_indexer(y2)
            self.apartment.u[0, y1: y2 + 1, x] = 273.15

        for j in range(len(self.apartment.t) - 1):
            self.apartment.u[j + 1, 1:-1, 1:-1] = self.apartment.u[j, 1:-1, 1:-1] + self.apartment.h_t * 0.025 * (
                    (self.apartment.u[j, 2:, 1:-1] - 2 * self.apartment.u[j, 1:-1, 1:-1] + self.apartment.u[j, :-2, 1:-1]) / self.apartment.h_x ** 2 +
                    (self.apartment.u[j, 1:-1, 2:] - 2 * self.apartment.u[j, 1:-1, 1:-1] + self.apartment.u[j, 1:-1, :-2]) / self.apartment.h_x ** 2)

            for x1, x2, y1, y2, rx1, rx2, ry1, ry2 in self.apartment.heaters:
                heater_area = (x2 - x1) * (y2 - y1)
                x1 = self.x_indexer(x1)
                x2 = self.x_indexer(x2)
                y1 = self.y_indexer(y1)
                y2 = self.y_indexer(y2)
                rx1 = self.x_indexer(rx1)
                rx2 = self.x_indexer(rx2)
                ry1 = self.y_indexer(ry1)
                ry2 = self.y_indexer(ry2)
                avg_temp = self.apartment.u[j, ry1 + 1: ry2, rx1 + 1: rx2].mean()
                heat = (avg_temp <= self.apartment.avg_temp_lim) * self.apartment.h_t * self.apartment.power / (1.1225 * heater_area * 1005)
                self.apartment.u[j + 1, y1: y2 + 1, x1: x2 + 1] += heat
                self.apartment.energy_usage += heat # * heater_area * self.apartment.h_t


            for x1, x2, y in self.apartment.x_walls:
                x1 = self.x_indexer(x1)
                x2 = self.x_indexer(x2)
                y = self.y_indexer(y)
                self.apartment.u[j + 1, y + 1, x1: x2 + 1] = self.apartment.u[j + 1, y + 2, x1: x2 + 1]
                self.apartment.u[j + 1, y - 1, x1: x2 + 1] = self.apartment.u[j + 1, y - 2, x1: x2 + 1]

                if x1 != 0:
                    self.apartment.u[j + 1, y, x1 - 1] = self.apartment.u[j + 1, y, x1 - 2]

                if x2 != self.apartment.u.shape[2] - 1:
                    self.apartment.u[j + 1, y, x2 + 1] = self.apartment.u[j + 1, y, x2 + 2]

            for x, y1, y2 in self.apartment.y_walls:
                x = self.x_indexer(x)
                y1 = self.y_indexer(y1)
                y2 = self.y_indexer(y2)
                self.apartment.u[j + 1, y1: y2 + 1, x + 1] = self.apartment.u[0, y1: y2 + 1, x + 2]
                self.apartment.u[j + 1, y1: y2 + 1, x - 1] = self.apartment.u[0, y1: y2 + 1, x - 2]

                if y1 != 0:
                    self.apartment.u[j + 1, y1 - 1, x] = self.apartment.u[j + 1, y1 - 2, x]

                if y2 != self.apartment.u.shape[1] - 1:
                    self.apartment.u[j + 1, y2 + 1, x] = self.apartment.u[j + 1, y2 + 2, x]

            self.apartment.u[j + 1, 0, :] = self.apartment.u[j + 1, 1, :]
            self.apartment.u[j + 1, -1, :] = self.apartment.u[j + 1, -2, :]
            self.apartment.u[j + 1, :, 0] = self.apartment.u[j + 1, :, 1]
            self.apartment.u[j + 1, :, -1] = self.apartment.u[j + 1, :, -2]

            for x1, x2, y in self.apartment.x_windows:
                x1 = self.x_indexer(x1)
                x2 = self.x_indexer(x2)
                y = self.y_indexer(y)
                self.apartment.u[j + 1, y, x1: x2 + 1] = self.apartment.avg_temp_outside

            for x, y1, y2 in self.apartment.y_windows:
                x = self.x_indexer(x)
                y1 = self.y_indexer(y1)
                y2 = self.y_indexer(y2)
                self.apartment.u[j + 1, y1: y2 + 1, x] = self.apartment.avg_temp_outside

            for x1, x2, y in self.apartment.x_walls:
                x1 = self.x_indexer(x1)
                x2 = self.x_indexer(x2)
                y = self.y_indexer(y)
                self.apartment.u[j + 1, y, x1: x2 + 1] = 273.15

            for x, y1, y2 in self.apartment.y_walls:
                x = self.x_indexer(x)
                y1 = self.y_indexer(y1)
                y2 = self.y_indexer(y2)
                self.apartment.u[j + 1, y1: y2 + 1, x] = 273.15
