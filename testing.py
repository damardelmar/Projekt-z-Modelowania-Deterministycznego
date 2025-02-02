import numpy as np
import matplotlib.pyplot as plt
from kod import Apartment
from kod import Visualiser
from kod import Solver

def f(x, y):
    return 273.15 - 10

"""
a = Apartment(6, 4, 4 * 60, f, 0, avg_temp_outside=-10)
a.add_x_wall(0, 3.5, 2)
a.add_x_wall(4.25, 6, 2)

a.add_x_wall(3, 3.5, 3)
a.add_x_wall(4.25, 6, 3)

a.add_y_wall(3, 2.75, 4)
a.add_y_wall(3, 2, 2.25)

a.add_x_window(4, 5, 0)
a.add_y_window(0, .5, 1.5)
a.add_y_window(0, 2.5, 3.5)

a.add_heater(.25, .5, 0.5, 1.5, 0, 6, 0, 2)
a.add_heater(.25, .5, 2.5, 3.5, 0, 3, 2, 4)
a.add_heater(4, 5, .25, .5, 0, 6, 0, 2)

v = Visualiser(a)
s = Solver(a)
s.solve()
v.draw()

v.plot_heatmap(0)
v.animate_solution()
v.plot_heatmap(1)
"""

b = Apartment(6, 4, 2 * 60, f, 2000, avg_temp_outside=-10)
b.add_x_wall(0, 3.5, 2)
b.add_x_wall(4.25, 6, 2)

b.add_x_wall(3, 3.5, 3)
b.add_x_wall(4.25, 6, 3)

b.add_y_wall(3, 2.75, 4)
b.add_y_wall(3, 2, 2.25)

b.add_x_window(4, 5, 0)
b.add_y_window(0, .5, 1.5)
b.add_y_window(0, 2.5, 3.5)

b.add_heater(.25, .5, 0.5, 1.5, 0, 6, 0, 2)
b.add_heater(.25, .5, 2.5, 3.5, 0, 3, 2, 4)
b.add_heater(4, 5, .25, .5, 0, 6, 0, 2)
b.add_heater(5.5, 5.75, 3.6, 3.9, 5.2, 6, 3.5, 4)

v = Visualiser(b)
v.draw()
s = Solver(b)
s.solve()

v.plot_heatmap(0)
v.animate_solution()
v.plot_heatmap(1)
