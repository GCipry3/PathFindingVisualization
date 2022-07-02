import sys
from tkinter import messagebox

import pygame

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows


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
        self.neighbours = []
        self.prior = None
        self.color = (50, 50, 50)

    def draw(self):
        self.updateColor()
        pygame.draw.rect(window, self.color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def updateColor(self):
        if self.isQueued:
            self.color = (150, 150, 0)
        if self.isVisited:
            self.color = (0, 150, 150)
        if self.inPath:
            self.color = (150, 0, 200)
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
        for i in range(columns):
            tmp = []
            for j in range(rows):
                tmp.append(Box(i, j))
            self.grid.append(tmp)

    def set_neighbours(self):
        for boxList in self.grid:
            for box in boxList:
                x = box.x
                y = box.y
                if x > 0:
                    box.neighbours.append(self.grid[x - 1][y])
                if x < columns - 1:
                    box.neighbours.append(self.grid[x + 1][y])
                if y > 0:
                    box.neighbours.append(self.grid[x][y - 1])
                if y < rows - 1:
                    box.neighbours.append(self.grid[x][y + 1])

    def drawGrid(self):
        for boxList in self.grid:
            for box in boxList:
                box.draw()


def getMouseCoords():
    return pygame.mouse.get_pos()


def getGridIndexWithCoords(x, y):
    return x // box_width, y // box_height


class PathFinding:
    def __init__(self):
        self.gridObject = Grid()
        self.targetIsSet = False
        self.target = None
        self.start = self.gridObject.grid[0][0]
        self.start.isStart = True
        self.begin_search = False
        self.searching = False

        self.queue = [self.start]
        self.path = []

    def reset(self):
        self.gridObject=Grid()
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

                if event.buttons[0]:
                    if (not currentBox.isStart) and (not currentBox.isTarget):
                        currentBox.isWall = True

                if event.buttons[2] and (not self.targetIsSet):
                    if (not currentBox.isWall) and (not currentBox.isStart):
                        self.targetIsSet = True
                        self.target = currentBox
                        self.target.isTarget = True

            # we can begin the search only when enter is pressed and target is set
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                if self.targetIsSet:
                    self.begin_search = True
                    self.searching = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

        self.Dijkstra()

    def Dijkstra(self):
        if self.begin_search:
            if len(self.queue) > 0 and self.searching:
                currentBox = self.queue.pop(0)
                currentBox.isVisited = True

                if currentBox == self.target:
                    self.searching = False
                    while currentBox.prior != self.start:
                        self.path.append(currentBox.prior)
                        currentBox = currentBox.prior
                        currentBox.inPath = True
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

    def draw(self):
        self.gridObject.drawGrid()

    def run(self):
        while True:
            self.update()
            self.draw()
            pygame.display.update()


def main():

    pathFinder = PathFinding()
    pathFinder.run()


main()
