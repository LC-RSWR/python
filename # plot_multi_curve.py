# plot_multi_curve.py
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(1, 10 * np.pi, 10)
y_1 = x
y_2 = np.square(x)
y_3 = np.log(x)
y_4 = np.sin(x)
y_5 = np.exp(x)
plt.plot(x,y_1)
plt.plot(x,y_2)
plt.plot(x,y_3)
plt.plot(x,y_4)
#plt.plot(x,y_5)
plt.show()