from math import *
from time import perf_counter
from xlsxwriter import Workbook
# import numpy as np
import matplotlib.pyplot as plt

XLS_FILENAME = 'fw_euler_output.xls' # file name of output
CREATE_PLOT = True # program creates a pyplot with the solution curve if True
CREATE_XLSX = True # program creates an Excel doc with point data in program directory if True


# the function on the right hand side of the differential equation y'=f(x,y)
def f(x: float, y: float) -> float:
    return log(x)-log(y) # (2,0; 2,25)
    # return -x*y/10+10
    # return 2*sin(y) - x


# step length (recommended 10^-7 < h < 10^-2)
h = 10**-3

# start at (x0, y0)
x0 = 0
y0 = 5

# stop at xstop
xstop = 10

# variables for x and y
x = x0
y = y0

# list containing the points of the solution curve
xylist = [(x0, y0)]

print('Calculating points on solution curve')

# note the time before the calculations
t1 = perf_counter()

# calculate the points in the solution curve
while x <= xstop:
    # compute the next y (y_n+1 = y_n + y'(x_n)) * h)
    try:
        y += f(x, y) * h
    except ValueError:
        print('Error in calculation. y might have grown too large')
    except ZeroDivisionError:
        print('Error in calculation. Attempted to divide by zero')

    # increment x (to x_n+1)
    x += h

    # append the point (x_n+1, y_n+1) to the list
    xylist.append((x, y))

# note the time after the calculations
t2 = perf_counter()

print('Done. Calculated', len(xylist), 'points in', round(t2 - t1, ndigits=4), 'seconds')

if CREATE_XLSX:
    # open a xls doc for writing points to
    print('Creating Excel sheet:', XLS_FILENAME + "...")
    wb = Workbook(XLS_FILENAME)
    ws = wb.add_worksheet(name='Output')

    ws.write_column('A1', data=[point[0] for point in xylist])
    ws.write_column('B1', data=[point[1] for point in xylist])

    wb.close()
    print('Done')

if CREATE_PLOT:
    print('Preparing plot...')
    # prepare a pyplot to display the curve
    fig, ax = plt.subplots()

    ax.set(xlabel='x', ylabel='y', title=None)
    ax.grid()
    plt.title('Lösningskurva')
    ax.plot([point[0] for point in xylist], [point[1] for point in xylist])
    print('Done')
    plt.show()
