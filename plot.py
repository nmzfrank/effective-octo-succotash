import math
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

file = open('data.dat','r')
x_plot = []
y_plot = []
z_plot = []
line1 = file.readline()
line2 = file.readline()

records1 = line1.split()
records2 = line2.split()

for index in range(len(records1)):
	longitude = math.radians(float(records1[index]))
	latitude = math.radians(float(records2[index]))
	x_plot.append(math.cos(latitude) * math.cos(longitude))
	y_plot.append(math.cos(latitude) * math.sin(longitude))
	z_plot.append(math.sin(latitude))

ax = plt.subplot(111,projection='3d')

ax.scatter(x_plot[:100],y_plot[:100],z_plot[:100])
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

plt.show()
