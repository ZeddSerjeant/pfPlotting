"""
Allows the data to be plotted in the same way as it used to be, but with Python, so that the number of technologies / languages is kept to a minimum. Though of course, with extra development,
the data should be able to be exported such that existing tech for the system can continue to be used

Zeddicaius Pearson <serjeant.work@gmail.com>
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import LogNorm, Normalize, PowerNorm
from DataFormat import Experiment

class FruitData:
    def __init__(self, filename):
        """open filename and import the data. One column covers one unit of time, and contains intensity values that match internal frequencies"""
        self.filename = filename
        self.loadData()
        self.frequency_axis = [i for i in range(200,1300,10)]

    def loadData(self):
        self.data = np.loadtxt(self.filename,dtype=np.int16,delimiter=",")

    def numMeasurements(self):
        return len(self.data[0,:])

    def plotDataAsMesh(self, interactive=True): #XXX enable backend to use image for other purposes
        fig, ax = plt.subplots()
        side_length = np.arange(self.numMeasurements())
        x_axis, y_axis = np.meshgrid(side_length, self.frequency_axis)
        mesh = ax.pcolormesh(x_axis,y_axis,self.data, norm=PowerNorm(0.4), cmap=cm.jet, shading='gouraud')
        fig.colorbar(mesh)
        ax.set_title("James Fruit Test, 27/11::4/12 - Mesh Plot")
        plt.show()
    # def plotDataAsRender(self, width=2000, interactive=True):
    #     fig, ax = plt.subplots()
    #     side_length = np.arange(width)
    #     x_axis, y_axis = np.meshgrid(side_length, self.frequency_axis)
    #     z_axis = self.data[::2] #XXX get every second row (Change this later James' code no longer does this)
    #     render = ax.imshow(z_axis, extent=(np.amin(x_axis), np.amax(x_axis), np.amin(y_axis), np.amax(y_axis)), cmap=cm.jet, norm=PowerNorm(0.4), interpolation="gaussian")
    #     fig.colorbar(render)
    #     ax.set_title("James Fruit Test, 27-29 - Image Render")
    #     plt.show()

fruit = FruitData("./data/fruit_data.csv")
fruit.plotDataAsMesh(interactive=True)
#fruit.plotDataAsRender(interactive=True)
