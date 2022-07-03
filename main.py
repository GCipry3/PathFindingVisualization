import sys
from tkinter import messagebox

import pygame

from Functions import timeIt

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

COLUMNS = 50
ROWS = 50

BOX_WIDTH = WINDOW_WIDTH // COLUMNS
BOX_HEIGHT = WINDOW_HEIGHT // ROWS

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.isStart = False
        self.isWall = False
        self.isTarget = False
        self.isQueued = False
        self.isVisited = False
        self.inPath = False

        self.prior = None
        self.neighbours = []

        self.color = (50, 50, 50)

    def draw(self):
        # before updating the color we set it with default value
        self.color = (50, 50, 50)

        self.updateColor()
        pygame.draw.rect(window, self.color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))

    def updateColor(self):
        if self.isQueued:
            self.color = (150, 150, 0)
        if self.isVisited:
            self.color = (0, 150, 150)
        if self.inPath:
            self.color = (150, 0, 0)
        if self.isWall:
            self.color = (150, 150, 150)
        if self.isStart:
            self.color = (0, 200, 0)
        if self.isTarget:
            self.color = (200, 200, 0)


class Grid:
    def __init__(self):
        self.grid = []
        self.create_grid()
        self.set_neighbours()

    def create_grid(self):
        for i in range(COLUMNS):
            tmp = []
            for j in range(ROWS):
                tmp.append(Box(i, j))
            self.grid.append(tmp)

    def set_neighbours(self):
        for boxList in self.grid:
            for box in boxList:
                x = box.x
                y = box.y
                if x > 0:
                    box.neighbours.append(self.grid[x - 1][y])
                if x < COLUMNS - 1:
                    box.neighbours.append(self.grid[x + 1][y])
                if y > 0:
                    box.neighbours.append(self.grid[x][y - 1])
                if y < ROWS - 1:
                    box.neighbours.append(self.grid[x][y + 1])

    def drawGrid(self):
        for boxList in self.grid:
            for box in boxList:
                box.draw()


def getMouseCoords():
    return pygame.mouse.get_pos()


def getGridIndexWithCoords(x, y):
    return x // BOX_WIDTH, y // BOX_HEIGHT


class PathFinding:
    def __init__(self):
        self.gridObject = Grid()
        self.target = None
        self.start = self.gridObject.grid[0][0]
        self.start.isStart = True

        self.begin_search = False
        self.searching = False
        self.targetIsSet = False

        self.queue = [self.start]
        self.path = []

    def reset(self):
        self.gridObject = Grid()
        self.targetIsSet = False
        self.target = None
        self.start = self.gridObject.grid[0][0]
        self.start.isStart = True
        self.begin_search = False
        self.searching = False

        self.queue = [self.start]
        self.path = []

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = getMouseCoords()
                i, j = getGridIndexWithCoords(x, y)
                currentBox = self.gridObject.grid[i][j]

                # buttons[0] = left click
                if event.buttons[0]:
                    if (not currentBox.isStart) and (not currentBox.isTarget):
                        currentBox.isWall = True

                # buttons[1] = scroll click
                if event.buttons[1]:
                    if (not currentBox.isStart) and (not currentBox.isTarget):
                        currentBox.isWall = False

                # buttons[2] = right click
                if event.buttons[2] and (not self.targetIsSet):
                    if (not currentBox.isWall) and (not currentBox.isStart):
                        self.targetIsSet = True
                        self.target = currentBox
                        self.target.isTarget = True

            # we can begin the search only when "RETURN" is pressed and target is set
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.targetIsSet:
                    self.begin_search = True
                    self.searching = True

            # we can reset the canvas by pressing "r"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    @timeIt
    def Dijkstra(self):
        if len(self.queue) > 0 and self.searching:
            currentBox = self.queue.pop(0)
            currentBox.isVisited = True

            if currentBox == self.target:
                self.searching = False
                while currentBox.prior != self.start:
                    self.path.append(currentBox.prior)
                    currentBox = currentBox.prior
                    currentBox.inPath = True
                    self.begin_search = False
            else:
                for neighbour in currentBox.neighbours:
                    if (not neighbour.isQueued) and (not neighbour.isWall):
                        neighbour.isQueued = True
                        neighbour.prior = currentBox
                        self.queue.append(neighbour)
        else:
            if self.searching:
                messagebox.showerror("Error", "There is no solution")
                self.searching = False
                self.begin_search = False

    def draw(self):
        self.gridObject.drawGrid()

    def run(self):
        while True:
            self.update()
            if self.begin_search:
                self.Dijkstra()
            self.draw()
            pygame.display.update()


def main():
    pathFinder = PathFinding()
    pathFinder.run()


main()
