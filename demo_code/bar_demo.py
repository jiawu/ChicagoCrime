"""
Simple demo of a bar chart. Adapted from matplotlib example in gallery.
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


# Example data
people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
x_pos = np.arange(len(people))
performance = 3 + 10 * np.random.rand(len(people))
error = np.random.rand(len(people))

plt.bar(x_pos, performance, yerr=error, align='center', alpha=0.4)
plt.xticks(x_pos, people)
plt.ylabel('Performance')
plt.title('How fast do you want to go today?')

plt.show()