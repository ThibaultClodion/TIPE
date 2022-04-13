import pygame as pg
import random as r
from DrawerHelper import *

scale = 6

numAnts = 1000  # Number of Ants
eliteAntsPercentage = 5  # Percentage of elite Ants
initPheromone = 1.0  # Pheromone init value

# Food Variables
foodList = []
numFood = 4  # Amount of food
minFoodDistance = 20
maxFoodDistance = 100
foodAmounts = []
initialFoodAmount = 4

# Number of obstacles
numObstacles = 4000
freeSpace = 3  # Free space left around food & spawn

# Algorith parameters
alpha = 3  # Impact of pheromones
beta = 3  # Impact of the distance
q = 100  # Multiplier of the distance traveled
p = 0.0003  # local evaporation rate of pheromones
gp = 0.0007  # global evaporation rate of pheromones

dHelper = DrawerHelper("AntColonyOptimization Example", int(100 * scale), int(100 * scale))
clock = pg.time.Clock()
ants = []
matrix = []
spawnX, spawnY = 0, 0
iterations = 0

class Colony:

    def __init__(self, shouldPrint=True,
                 numFood=5,
                 minFoodDistance=20,
                 maxFoodDistance=25):
        self.shouldPrint = shouldPrint
        self.numFood = numFood  # Amount of food
        self.minFoodDistance = minFoodDistance
        self.maxFoodDistance = maxFoodDistance

        self.scale = 6
        self.numAnts = 1000  # Number of Ants
        self.eliteAntsPercentage = 5  # Percentage of elite Ants
        self.initPheromone = 1.0  # Pheromone init value

        # Food Variables
        self.foodList = []
        self.foodAmounts = []
        self.initialFoodAmount = 10

        # Number of obstacles
        self.numObstacles = 4000
        self.freeSpace = 3  # Free space left around food & spawn

        # Algorith parameters
        self.alpha = 3  # Impact of pheromones
        self.beta = 3  # Impact of the distance
        self.q = 100  # Multiplier of the distance traveled
        self.p = 0.0003  # local evaporation rate of pheromones
        self.gp = 0.0007  # global evaporation rate of pheromones

        self.dHelper = DrawerHelper("AntColonyOptimization Example", int(100 * self.scale), int(100 * self.scale))
        self.clock = pg.time.Clock()
        self.ants = []
        self.matrix = []
        self.spawnX, spawnY = 0, 0
        self.iterations = 0

    def __del__(self):
        del self.matrix
        del self.ants
        del self.clock
        del self.dHelper

    def getIterations(self):
        return self.iterations

    def getClock(self):
        return self.clock

    def getMatrix(self):
        return self.matrix

    def getInitPheromone(self):
        return self.initPheromone

    def getAlpha(self):
        return self.alpha

    def getBeta(self):
        return self.beta

    def getFoodAmounts(self):
        return self.foodAmounts

    def getFoodList(self):
        return self.foodList

    def getInitialFoodAmount(self):
        return self.initialFoodAmount

    def getP(self):
        return self.p

    def getQ(self):
        return self.q

    def getSpawn(self):
        return self.spawnX, self.spawnY

    # Field initialization
    def initField(self):
        for i in range(100):
            self.matrix.append([])
            for j in range(100):
                self.matrix[i].append(self.initPheromone)
        self.spawnX = r.randint(0, 99)
        self.spawnY = r.randint(0, 99)
        self.matrix[self.spawnX][self.spawnY] = "spawn"

        for i in range(self.numFood):
            putFoodSuccess = False
            while not putFoodSuccess:
                foodX = r.randint(5, 94)
                foodY = r.randint(5, 94)
                foodXSuccess = (abs(foodX - self.spawnX) in range(self.minFoodDistance, self.maxFoodDistance)) and (
                        abs(foodY - self.spawnY) in range(0, self.maxFoodDistance))
                foodYSuccess = (abs(foodY - self.spawnY) in range(self.minFoodDistance, self.maxFoodDistance)) and (
                        abs(foodX - self.spawnX) in range(0, self.maxFoodDistance))
                if foodXSuccess or foodYSuccess:
                    if [foodX, foodY] not in self.foodList:
                        self.foodList.append([foodX, foodY])
                        self.foodAmounts.append(self.initialFoodAmount)
                        self.matrix[foodX][foodY] = "food"
                        putFoodSuccess = True

        for i in range(self.numObstacles):
            putObstacleSuccess = 0
            while putObstacleSuccess < self.numFood + 1:
                obstacleX = r.randint(0, 99)
                obstacleY = r.randint(0, 99)
                if not ((self.matrix[obstacleX][obstacleY] == "obstacle") and (
                        self.matrix[obstacleX][obstacleY] == "food") and (
                                self.matrix[obstacleX][obstacleY] == "spawn")):
                    spawnXSuccess = (obstacleX <= self.spawnX - self.freeSpace) or (
                            obstacleX >= self.spawnX + self.freeSpace)
                    spawnYSuccess = (obstacleY <= self.spawnY - self.freeSpace) or (
                            obstacleY >= self.spawnY + self.freeSpace)
                    if spawnXSuccess or spawnYSuccess:
                        putObstacleSuccess += 1
                    else:
                        putObstacleSuccess = 0
                        continue
                    for i in range(self.numFood):
                        foodX = self.foodList[i][0]
                        foodY = self.foodList[i][1]
                        foodXSuccess = (obstacleX <= foodX - self.freeSpace) or (obstacleX >= foodX + self.freeSpace)
                        foodYSuccess = (obstacleY <= foodY - self.freeSpace) or (obstacleY >= foodY + self.freeSpace)
                        if foodXSuccess or foodYSuccess:
                            putObstacleSuccess += 1
                        else:
                            putObstacleSuccess = 0
                            continue
            self.matrix[obstacleX][obstacleY] = "obstacle"

    # Draw field
    def drawField(self):
        self.dHelper.draw_background(self.dHelper.WHITE)
        for i in range(100):
            for j in range(100):
                if self.matrix[i][j] == "spawn":
                    self.dHelper.blit(self.dHelper.BLUE, 255, i, j, self.scale)
                elif self.matrix[i][j] == "food":
                    if self.initialFoodAmount > 0:
                        foodAlpha = self.foodAmounts[self.foodList.index([i, j])] / self.initialFoodAmount * 200 + 55
                    else:
                        foodAlpha = 255
                    self.dHelper.blit(self.dHelper.RED, foodAlpha, i, j, self.scale)

                elif self.matrix[i][j] == "obstacle":
                    self.dHelper.blit(self.dHelper.BLACK, 20, i, j, self.scale)
                else:
                    pheromoneGray = 255 - (self.matrix[i][j] - self.initPheromone) * 1.4
                    pheromoneGreen = 2 * pheromoneGray
                    if pheromoneGray > 255:
                        pheromoneGray = 255
                    if pheromoneGray < 0:
                        pheromoneGray = 0
                    if pheromoneGreen > 255:
                        pheromoneGreen = 255
                    if pheromoneGreen < 50:
                        pheromoneGreen = 50
                    self.dHelper.blit((pheromoneGray, pheromoneGreen, pheromoneGray), 255, i, j, self.scale)

    # Ants initialisation
    def createAnts(self):
        numLeet = int(self.eliteAntsPercentage / 100 * self.numAnts)  # Number of elite ants

        for i in range(self.numAnts):
            self.ants.append(Ant(self.spawnX,
                                 self.spawnY,
                                 False,
                                 self.shouldPrint))

        # Election of elite ants
        while numLeet > 0:
            leetCandidate = r.choice(self.ants)
            if not leetCandidate.leet:
                leetCandidate.leet = True
                numLeet -= 1
                if self.shouldPrint:
                    print("Ant: ", "%#10d" % leetCandidate.id, " became an elite !")

    # Moving & drawing the ants
    def drawAndMoveAnts(self, should_draw=True):
        for ant in self.ants:
            ant.turn(self)
            if should_draw:
                if not ant.leet:
                    self.dHelper.blit(self.dHelper.BLACK, 70, ant.x, ant.y, self.scale)
                else:
                    self.dHelper.blit(self.dHelper.TEAL, 127, ant.x, ant.y, self.scale)

    # Global evaporation of pheromones
    def globalEvaporate(self):
        for i in range(100):
            for j in range(100):
                if type(self.matrix[i][j]) == type(0.0):
                    self.matrix[i][j] *= (1 - self.gp);

    def noFood(self):
        if self.initialFoodAmount > 0:
            for i in self.foodAmounts:
                if i > 0:
                    return False
            return True
        else:
            return False

    def inc(self):
        self.iterations += 1


# Function to return the inverse of the distance
def getInverseDistance(dir_):
    if (dir_ == 0) or (dir_ == 2) or (dir_ == 4) or (dir_ == 6):
        return 1.0  # Straight line, distance == 1
    else:
        return float(1 / 2 ** .5)  # Diagonal distance


class Ant:
    def __init__(self, x, y, leet, shouldPrint):
        self.x = x
        self.y = y
        self.tabooList = []
        self.putPheromone = False
        self.l0 = 0
        self.tabooListIndex = 0
        self.leet = leet
        self.id = r.randint(10000000, 99999999)
        self.shouldPrint = shouldPrint

    def move(self, dir_):
        if [self.x, self.y] not in self.tabooList:
            self.tabooList.append([self.x, self.y])
        dx, dy = 0, 0

        if dir_ == 0:
            dy = -1
        if dir_ == 1:
            dy = -1
            dx = 1
        if dir_ == 2:
            dx = 1
        if dir_ == 3:
            dx = 1
            dy = 1
        if dir_ == 4:
            dy = 1
        if dir_ == 5:
            dy = 1
            dx = -1
        if dir_ == 6:
            dx = -1
        if dir_ == 7:
            dx = -1
            dy = -1

        self.x += dx
        self.y += dy

        if [self.x, self.y] not in self.tabooList:
            self.tabooList.append([self.x, self.y])

        if dx * dy == 0:
            self.l0 += 1
        else:
            self.l0 += 2 ** .5

    def tryMove(self, dir_):
        if dir_ == 0:
            return [self.x, self.y - 1]
        if dir_ == 1:
            return [self.x + 1, self.y - 1]
        if dir_ == 2:
            return [self.x + 1, self.y]
        if dir_ == 3:
            return [self.x + 1, self.y + 1]
        if dir_ == 4:
            return [self.x, self.y + 1]
        if dir_ == 5:
            return [self.x - 1, self.y + 1]
        if dir_ == 6:
            return [self.x - 1, self.y]
        if dir_ == 7:
            return [self.x - 1, self.y - 1]

    # Get the amount of pheromones on neighboring cells
    def getPheromone(self, matrix, initPheromone, dir_):
        pheromoneX = self.x
        pheromoneY = self.y
        if dir_ == 0:
            pheromoneY = self.y - 1
        if dir_ == 1:
            pheromoneY = self.y - 1
            pheromoneX = self.x + 1
        if dir_ == 2:
            pheromoneX = self.x + 1
        if dir_ == 3:
            pheromoneX = self.x + 1
            pheromoneY = self.y + 1
        if dir_ == 4:
            pheromoneY = self.y + 1
        if dir_ == 5:
            pheromoneY = self.y + 1
            pheromoneX = self.x - 1
        if dir_ == 6:
            pheromoneX = self.x - 1
        if dir_ == 7:
            pheromoneX = self.x - 1
            pheromoneY = self.y - 1

        if type(matrix[pheromoneX][pheromoneY]) == type(0.0):
            return matrix[pheromoneX][pheromoneY]
        else:
            return initPheromone * 10000

    # Determine possible moves
    possibleTurns = []

    def addPossibleTurns(self, matrix, arr):
        self.possibleTurns = []
        for i in arr:
            pp = self.tryMove(i)
            if not (pp in self.tabooList) and (pp[0] in range(0, 100)) and (pp[1] in range(0, 100)) and (
                    matrix[pp[0]][pp[1]] != "obstacle"):
                self.possibleTurns.append(i)

    # Resetting the ants when it's lost
    def respawn(self, spawn):
        self.x = spawn[0]
        self.y = spawn[1]
        self.tabooList = []
        self.putPheromone = False
        self.tabooListIndex = 0
        self.l0 = 0
        if self.shouldPrint:
            print("Ant: ", self.id, " respawned !")

    # Choose next point of interest and move there
    def turn(self, col: Colony):
        if not self.putPheromone:

            # Set possible directions
            if (self.x == 0) and (self.y == 0):
                self.addPossibleTurns(col.getMatrix(), [2, 3, 4])
            if (self.x == 0) and (self.y == 99):
                self.addPossibleTurns(col.getMatrix(), [0, 1, 2])
            if (self.x == 99) and (self.y == 0):
                self.addPossibleTurns(col.getMatrix(), [4, 5, 6])
            if (self.x == 99) and (self.y == 99):
                self.addPossibleTurns(col.getMatrix(), [6, 7, 0])
            if (self.x == 0) and (self.y in range(1, 99)):
                self.addPossibleTurns(col.getMatrix(), [0, 1, 2, 3, 4])
            if (self.x == 99) and (self.y in range(1, 99)):
                self.addPossibleTurns(col.getMatrix(), [0, 4, 5, 6, 7])
            if (self.y == 0) and (self.x in range(1, 99)):
                self.addPossibleTurns(col.getMatrix(), [2, 3, 4, 5, 6])
            if (self.y == 99) and (self.x in range(1, 99)):
                self.addPossibleTurns(col.getMatrix(), [6, 7, 0, 1, 2])
            if (self.x in range(1, 99)) and (self.y in range(1, 99)):
                self.addPossibleTurns(col.getMatrix(), [0, 1, 2, 3, 4, 5, 6, 7])

            # Calculate the prob of a move
            sum_ = 0
            probabilities = []
            for i in self.possibleTurns:
                sum_ += getInverseDistance(i) ** col.getBeta() * self.getPheromone(col.getMatrix(),
                                                                                   col.getInitPheromone(),
                                                                                   i) ** col.getAlpha()
            for i in self.possibleTurns:
                probabilities.append(
                    getInverseDistance(i) ** col.getBeta() * self.getPheromone(col.getMatrix(), col.getInitPheromone(),
                                                                               i) ** col.getAlpha() / sum_)

            if not self.leet:
                # Function to calculate the sum of the first elements of the array
                def sumFirstElements(arr, end):
                    summ = 0
                    if end >= len(arr):
                        end = len(arr) - 1
                    for i in range(0, end):
                        summ += arr[i]
                    return summ

                # Randomly choosing the direction
                probRange = []
                for i in range(0, len(probabilities)):
                    probRange.append(sumFirstElements(probabilities, i))

                def selectDir():
                    if len(self.possibleTurns) > 0:
                        rand = r.random()
                        for i in range(len(probRange) - 1):
                            if (rand >= probRange[i]) and (rand < probRange[i + 1]):
                                return self.possibleTurns[i]
                        if rand >= probRange[-1]:
                            return self.possibleTurns[-1]
                    else:
                        self.respawn(col.getSpawn())
            else:
                def selectDir():
                    if len(self.possibleTurns) > 0:
                        maxProb = max(probabilities)
                        maxIndexes = [i for i, j in enumerate(probabilities) if j == maxProb]
                        return self.possibleTurns[r.choice(maxIndexes)]
                    else:
                        self.respawn(col.getSpawn())

            newDir = selectDir()
            self.move(newDir)

            if col.getMatrix()[self.x][self.y] == "food":
                antStr = "Ant:"
                if self.leet:
                    antStr = "Elite Ant:"
                if self.shouldPrint:
                    print(antStr, self.id, " found",
                          "%#3d" % col.getFoodAmounts()[col.getFoodList().index([self.x, self.y])],
                          "food units at coordinate :", self.x, self.y, "in", "%#10f" % self.l0, "steps")
                self.putPheromone = True

                if col.getInitialFoodAmount() != 0:
                    col.getFoodAmounts()[col.getFoodList().index([self.x, self.y])] -= 1
                    if col.getFoodAmounts()[col.getFoodList().index([self.x, self.y])] == 0:
                        col.getMatrix()[self.x][self.y] = col.getInitPheromone()
                        self.putPheromone = False
                        if self.shouldPrint:
                            print("The food at : ", self.x, self.y, " is finished but the pheromones remains.")

        else:  # if putFeromone
            self.tabooListIndex += 1
            self.x = self.tabooList[-self.tabooListIndex][0]
            self.y = self.tabooList[-self.tabooListIndex][1]

            if type(col.getMatrix()[self.x][self.y]) == type(0.0):
                newTau = (1 - col.getP()) * col.getMatrix()[self.x][self.y] + col.getQ() / self.l0
                col.getMatrix()[self.x][self.y] = newTau

            if col.getMatrix()[self.x][self.y] == "spawn":
                self.respawn(col.getSpawn())
        return


def main():
    shouldPrint = True
    ant_colony = Colony(shouldPrint)
    ant_colony.initField()
    ant_colony.createAnts()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        ant_colony.drawField()
        ant_colony.drawAndMoveAnts()
        pg.display.flip()
        ant_colony.getClock().tick()
        ant_colony.globalEvaporate()
        ant_colony.inc()
        if ant_colony.noFood():
            if shouldPrint:
                print("Ants have eaten all the food in : ", ant_colony.getIterations(), "iterations.")
            running = False
    pg.quit()


if __name__ == "__main__":
    main()
