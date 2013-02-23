"""
A PyrobotSimulator world. A room with one obstacle and
a small inner room.

(c) 2005, PyroRobotics.org. Licensed under the GNU GPL.
"""

from pyrobot.simulators.pysim import *
from pyrobot.maze.Maze import *
from pyrobot.maze.MazeDrawer import *
from pyrobot.maze.MazeDrawerPyro import *

def INIT():
    # (width, height), (offset x, offset y), scale:
    sim = TkSimulator((650, 650), (25, 625), 60)
    maze_drawer = MazeDrawer(10.0, 10.0)
    maze_drawer.draw(Maze(10, 10), MazeDrawerPyro(sim))

    # port, name, x, y, th, bounding Xs, bounding Ys, color
    # (optional TK color name):
    sim.addRobot(60000, TkPioneer("BluePioneer",
                                  .5, .5, 0.00,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175)),
                                    "deepskyblue"))
    # add some sensors:
    #sim.robots[0].addDevice(PioneerFrontSonars()) # for 8 front sonar
    sim.robots[0].addDevice(Pioneer16Sonars()) # for full 360 sonar

    return sim

