# First, let's dig deeper into understanding how imports work
# Open up your command window and start the interpreter

# We've already worked with pyplot from matplotlib, so let's work with that
# There are many options for importing packages and modules. We will work with a few

# ==============================================================================
# ==============================================================================
# In the interpreter
# ==============================================================================
# ==============================================================================
# Let's make some data to work with
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# Now we'll import matplotlib.pyplot. Notice that this is slightly different
# then how we did it in the plotting example
import matplotlib.pyplot

# We can use all the methods in the module
matplotlib.pyplot.plot(x, y)
matplotlib.pyplot.show()

# This works, but it ends up being a lot of typing. Python is prepared to save
# my finger strength

import matplotlib.pyplot as plt

# With the "as" statement, we've created an alias for the module import.
# plt will behave the same way that matplotlib.pyplot would, with much less typing.
plt.plot(x,y)
plt.show()

# There are many common package abbreviations. In fact, we saw another before as well
import numpy as np

# We can also import methods or objects directly from the package
from matplotlib.pyplot import plot
plot(x,y)

# This makes a plot object, but we have no way to render it. We have to directly
# import the show function
from matplotlib.pyplot import show
show()

# We could have bundled those together into one line as well
from matplotlib.pyplot import plot, show

# Lastly, something that gets used all the time is importing all of the methods
# from a module
from matplotlib.pyplot import *

# The "*" specifies importing every single function from the module. You should
# be careful using this, because there may be overlap between method names and
# variables you might use.

# For example "show" is a function in pyplot
show

# If we were to make a variable show, it would overwrride the function  in the
# namespace
show = 8
show

# So be careful!

# Now we'll use what we've just learned to refactor our project into something
# easier to use

# Continue in "creating_the_main_file.py"




