import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
x_data = []
y_data = []

line, = ax.plot([], [], lw=2)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return line,

def update(frame):
    x_data.append(frame)
    y_data.append(np.sin(frame))
    line.set_data(x_data, y_data)
    return line,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)

plt.show()