import matplotlib.pyplot as plt 
import numpy as np

x = np.linspace(-10, 10, 200)

y = -x**2 - 5 

plt.plot(x, y)
plt.title("f(x) = -x² - 5")
plt.grid(True)
plt.show()
