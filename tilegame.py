import numpy as np
from enum import IntEnum, auto

class KeyMap:
    UP = (-1,0)
    DOWN = (1,0)
    LEFT = (0,-1)
    RIGHT = (0,1)

class MapObj:
    FREE = 0
    ME = 1
    WALL = 2
    FLUIT = 3

class TileGame:
    def __init__(self, mapfile, coordinate=(1,1)):
        self.reward = 100
        self.mapfile = mapfile
        self.origincoordinate = coordinate
        self.coordinate = coordinate
        self.map = np.loadtxt(mapfile,delimiter=",")
        self.map[(self.coordinate)] = 1
    def reset(self):
        self.coordinate = self.origincoordinate
        self.map = np.loadtxt(self.mapfile,delimiter=",")
        self.map[(self.coordinate)] = 1
        return self.map
    def step(self, action):
        observation = self.map
        reward = 0
        done = False

        nextCoorde = tuple(np.array([0,0]) + self.coordinate + action)
        if (0 <= nextCoorde[0] and self.map.shape[0] > nextCoorde[0]
            and 0 <= nextCoorde[1] and self.map.shape[1] > nextCoorde[1]):
            # not overed array
            nextObj = self.map[nextCoorde]
            if (nextObj != MapObj.WALL):
                # not hitting wall
                if (nextObj == MapObj.FLUIT):
                    # hitting fruit
                    reward = self.reward
                    done = True
                # update map and self coordinate
                self.updateMap(nextCoorde)
        return observation, reward, done
    def updateMap(self, nextCoorde):
        self.map[self.coordinate] = MapObj.FREE
        self.map[nextCoorde] = MapObj.ME
        self.coordinate = nextCoorde
if __name__ == "__main__":
    env = TileGame("../assets/grid2.csv")
    observation = env.reset()
    np.set_printoptions(linewidth=200)
    print(observation)
    while True:
        action = input("UP:1, DOWN:2, LEFT:3, RIGHT:4 : ")
        if action == "1":
            act = KeyMap.UP
        elif action == "2":
            act = KeyMap.DOWN
        elif action == "3":
            act = KeyMap.LEFT
        elif action == "4":
            act = KeyMap.RIGHT
        else:
            print("invalid input")
            continue

        observation, reward, done = env.step(act)
        print("reward : {} \n done : {}".format(reward, done))
        print(observation)

