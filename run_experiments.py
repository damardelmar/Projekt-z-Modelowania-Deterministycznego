from kod import Apartment
from kod import Visualiser
from kod import Solver


def f(x, y):
    return 273.15 + 5


a = Apartment(4, 4, 120, f, 1500)

a.add_y_window(0, 1.5, 2.5)
#a.add_heater(0.25, 0.5, 1.5, 2.5, 0, 4, 0, 4)
a.add_heater(3.5, 3.75, 1.5, 2.5, 0, 4, 0, 4)
#a.add_heater(1.9, 2.1, 1.5, 2.5, 0, 4, 0, 4)
s = Solver(a)
s.solve()

v = Visualiser(a)
v.draw()
v.plot_heatmap(1)
v.animate_solution()

###
a = Apartment(4, 4, 120, f, 1500)

a.add_y_window(0, 1.5, 2.5)
#a.add_heater(0.25, 0.5, 1.5, 2.5, 0, 4, 0, 4)
#a.add_heater(3.5, 3.75, 1.5, 2.5, 0, 4, 0, 4)
a.add_heater(1.9, 2.1, 1.5, 2.5, 0, 4, 0, 4)
s = Solver(a)
s.solve()

v = Visualiser(a)
v.draw()
v.plot_heatmap(1)
v.animate_solution()

###
a = Apartment(4, 4, 120, f, 1500)

a.add_y_window(0, 1.5, 2.5)
a.add_heater(0.25, 0.5, 1.5, 2.5, 0, 4, 0, 4)
#a.add_heater(3.5, 3.75, 1.5, 2.5, 0, 4, 0, 4)
#a.add_heater(1.9, 2.1, 1.5, 2.5, 0, 4, 0, 4)
s = Solver(a)
s.solve()

v = Visualiser(a)
v.draw()
v.plot_heatmap(1)
v.animate_solution()


###
def f(x, y):
    return 273.15 - 10


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

v.animate_solution()
v.plot_heatmap(1)

b = Apartment(6, 4, 60, f, 1500, avg_temp_outside=-10)
b.u[0, :, :] = a.u[-1, :, :]
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
b.add_heater(5.5, 5.75, 3.6, 3.9, 3, 6, 3, 4)

v = Visualiser(b)
v.draw()
s = Solver(b)
s.solve()

v.animate_solution()
v.plot_heatmap(1)


###
def f(x, y):
    return 273.15 + 20


for m in [-10, 0, 5]:
    a = Apartment(6, 4, 2 * 60, f, 0, avg_temp_outside=m)
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


    b = Apartment(6, 4, 20, f, 2000, avg_temp_outside=m)
    b.u[0, :, :] = a.u[-1, :, :]
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
    s = Solver(b)
    s.solve()

    v.plot_heatmap(0)
    v.animate_solution()
    v.plot_heatmap(1)


for m in [-10, 0, 5]:
    a = Apartment(6, 4, 2 * 60, f, 2000, avg_temp_outside=m)
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
