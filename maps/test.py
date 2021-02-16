import matplotlib.pyplot as plt
import numpy as np


# example of 
fig, ax = plt.subplots(3,3)

axx = ax.flatten()
for i in range(9):
    axx[i].imshow(np.random.rand(10, 10))
    if i in [0, 1, 2]:
        axx[i].set_title('test')


# make a colorbar on its own
fig = plt.figure()
cx0 = fig.add_axes([.1, .1, .8, .015])
cx1 = fig.add_axes([.1, .37, .8, .015])
cx2 = fig.add_axes([.1, .7, .8, .015])
fig.colorbar(c0, cax=cx0, orientation='horizontal')
fig.colorbar(c1, cax=cx1, orientation='horizontal')
fig.colorbar(c2, cax=cx2, orientation='horizontal')