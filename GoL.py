import random
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt, animation


class GameOfLife:
    def __init__(self, N=50):
        # create map with specified rows/cols
        self.grid = np.zeros((N, N), np.int8)
        self.rows = N
        self.cols = N

        # neighbourhood (nbhd) pattern around each cell
        self.nbhd = np.ones((3, 3), np.int8)
        self.nbhd[1, 1] = 0

        # alive and dead values of each cell
        self.alive = 1
        self.dead = 0

    def getMap(self):
        """Return the current GOL map"""
        return self.grid

    def randomlyPopulateMap(self):
        """Randomly populate the current GOL map"""
        for row in range(self.rows):
            for col in range(self.cols):
                populate = random.randint(0, 1)
                if populate:
                    self.grid.itemset((row, col), self.alive)

    def update(self):
        """Given the current states of the cells within the grid, apply the four Game of Life rules."""
        # generate new blank grid
        newGrid = np.zeros((self.rows, self.cols), np.int8)

        # use a convolution to compute status of neighbours around each cell
        scores = signal.convolve2d(self.grid, self.nbhd, mode="same", boundary="wrap", fillvalue=0)

        # iterate over whole existing grid
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                cell = self.grid.item(row, col)
                score = scores.item(row, col)

                if cell == self.dead and score == 3:  # (rule 1) reproduction
                    newGrid.itemset((row, col), self.alive)
                elif cell == self.alive:
                    if score < 2:  # (rule 2) underpopulation
                        newGrid.itemset((row, col), self.dead)
                    elif score == 2 or score == 3:  # (rule 3) cells that continue to live
                        newGrid.itemset((row, col), self.alive)
                    elif score > 3:  # (rule 4) overpopulation
                        newGrid.itemset((row, col), self.dead)

        # update the grid
        self.grid = newGrid


def animate(i):
    """perform a step in the animation"""
    global life

    life.update()
    cellsUpdated = life.getMap()

    img.set_array(cellsUpdated)

    return img,

if __name__ == "__main__":
    # create an empty figure
    fig = plt.figure()

    # create Game of Life instance
    life = GameOfLife()
    # randomly populate the map
    life.randomlyPopulateMap()

    # configure animation
    cells = life.getMap()
    img = plt.imshow(cells, animated=True, cmap=plt.get_cmap("cividis"))
    anim = animation.FuncAnimation(fig, animate, frames=24, repeat=True, interval=250, blit=True)

    # save video
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    anim.save('GOL.gif', writer=writer)

    # show animation
    plt.show()
