# Jacob Auman
# 10-19-23
# This file is a silly test to plot out all of the different Curl 1 Rep Max Formulas

import matplotlib.pyplot as plt
import numpy as np

# Define the formulas
def brzycki(weight, reps):
    return weight * (36 / (37 - reps))

def epley(weight, reps):
    return weight * (1 + reps / 30)

def lander(weight, reps):
    return (100 * weight) / (101.3 - 2.67123 * reps)

def lombardi(weight, reps):
    return weight * reps ** 0.1

def mayhew(weight, reps):
    return (100 * weight) / (52.2 + 41.9 * np.exp(-0.055 * reps))

def oconner(weight, reps):
    return weight * (1 + reps / 40)

def wathan(weight, reps):
    return (100 * weight) / (48.8 + 53.8 * np.exp(-0.075 * reps))

# Create some sample data that considers the median number of reps around (12) and the weight (25 lbs)
x = np.arange(1, 20, 0.1)
y = np.full(len(x), 25)



# Plot the data
plt.plot(x, brzycki(y, x), label='Brzycki')
plt.plot(x, epley(y, x), label='Epley')
plt.plot(x, lander(y, x), label='Lander')
plt.plot(x, lombardi(y, x), label='Lombardi')
plt.plot(x, mayhew(y, x), label='Mayhew')
plt.plot(x, oconner(y, x), label='O\'Conner')
plt.plot(x, wathan(y, x), label='Wathan')

# Add a legend
plt.legend()

# Add labels
plt.xlabel('Reps')
plt.ylabel('Weight')

# Show the plot
plt.show()

