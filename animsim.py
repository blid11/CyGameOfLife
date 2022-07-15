import math

import matplotlib.pyplot as plt
from itertools import product, combinations
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation

import collections
import csv

class AnimSim:
    #no initializer, just pass data
    """
    Need to be able to 
    """

    data = []

    def anim_vid(self, sim_string):

        # data = self.data


        if self.generation > 50:
            data = []

            for generation in range(0, 50):
                data.append(self.data[generation])

        else:
            data = self.data

        # print("THIS SHOULD ANIMATE")

        # print(data)


        """
        Creates the 3D figure and animates it with the input data.
        Args:
            data (list): List of the data positions at each iteration.
            save (bool): Whether to save the recording of the animation. (Default to False).
        """

        # print(data)

        # Number of iterations
        iterations = len(data)
        # print(iterations)

        # Attaching 3D axis to the figure
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        # Initialize scatters
        # scatters = [ax.scatter(data[0][i, 0:1], data[0][i, 1:2], data[0][i, 2:]) for i in range(data[0].shape[0])]
        for cell in self.data[0]:
            ax.scatter(cell[0], cell[1], cell[2])

        def animate_scatters(frame):
            """
            Update the data held by the scatter plot and therefore animates it.
            Args:
                iteration (int): Current iteration of the animation
                data (list): List of the data positions at each iteration.
                scatters (list): List of all the scatters (One per element)
            Returns:
                list: List of scatters (One per element) with new coordinates
            """

            ax.clear()

            ax.set_xlim3d([40, 90])
            ax.set_xlabel('X')

            ax.set_ylim3d([40, 90])
            ax.set_ylabel('Y')

            ax.set_zlim3d([40, 90])
            ax.set_zlabel('Z')

            ax.set_title(sim_string)

            # Provide starting angle for the view.
            ax.view_init(25, -90)

            # scatters.clear()

            for cell in self.data[frame]:
                ax.scatter(cell[0], cell[1], cell[2])

            # scatters = [ax.scatter(data[frame][i, 0:1], data[frame][i, 1:2], data[frame][i, 2:]) for i in range(data[frame].shape[1])]
            #
            # return scatters


        # Setting the axes properties
        ax.set_xlim3d([40, 90])
        ax.set_xlabel('X')

        ax.set_ylim3d([40, 90])
        ax.set_ylabel('Y')

        ax.set_zlim3d([40, 90])
        ax.set_zlabel('Z')

        ax.set_title(sim_string)

        # Provide starting angle for the view.
        ax.view_init(25, -90)

        def init_func():
            ax.clear()

            ax.set_xlim3d([40, 90])
            ax.set_xlabel('X')

            ax.set_ylim3d([40, 90])
            ax.set_ylabel('Y')

            ax.set_zlim3d([40, 90])
            ax.set_zlabel('Z')

            ax.set_title(sim_string)

            # Provide starting angle for the view.
            ax.view_init(25, -90)
            # scatters.clear()

        ani = animation.FuncAnimation(fig, animate_scatters, frames=iterations,
                                      interval=200, blit=False, repeat=False,  init_func=init_func)

        # ani = animation.FuncAnimation(fig, animate_scatters, frames=iterations,
        #                               interval=200, blit=False, repeat=True, init_func=init_func)
        # matplotlib may not immediately show the animation but the saved mp4 should show it

        save = True

        if save:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec','libx264'])
            ani.save(sim_string + '.mp4', writer=writer)

        plt.show()
        #
        plt.close()
