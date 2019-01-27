#code created by Benjamin Hatch and Riley Parkerson in 2018...Senior Year at Granada High School
#anyone can use this for inspiration
import pygame as pg
import random

timer = pg.time.Clock()

screen = pg.display.set_mode((800, 600))
# variables
highlightTimer = 0
highlightTick = 0
rowHighlight = False
holdDownTimer = 25
holdRightTimer = 25
holdLeftTimer = 25
holdDown = False
holdLeft = False
holdRight = False
fallTimer = 0
fallSpeed = 500
run = True
level = 1
lines = 0
score = 0
blockSize = 30
playWidth = 300
playHeight = 600
playX = (800 - playWidth) // 2
playY = (800 - playHeight) // 2
Loss = False
nextShape = True
newCoords = [0, 0, 0, 0, 0, 0, 0, 0]
currentShape = 0
gameOver = False
gamePaused = False
dGO = 0
#turnSound = pg.mixer.Sound("images/TetrisTurnSound.wav")
#rowSound = pg.mixer.Sound("images/TetrisRowSound.wav")

screen.blit(pg.image.load("images/TetrisUi.png"), (0, 0))

# colors
RED = (255, 0, 0)
ORANGE = (255, 185, 30)
YELLOW = (255, 255, 30)
GREEN = (30, 255, 30)
BLUE = (30, 30, 255)
PURPLE = (215, 30, 255)
LIGHTBLUE = (100, 200, 255)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BGCOLOR = (0, 24.2, 37.8)

numberImages = [pg.image.load("images/Tetris0.png"), pg.image.load("images/Tetris1.png"), pg.image.load("images/Tetris2.png"),
               pg.image.load("images/Tetris3.png"), pg.image.load("images/Tetris4.png"), pg.image.load("images/Tetris5.png"),
               pg.image.load("images/Tetris6.png"), pg.image.load("images/Tetris7.png"), pg.image.load("images/Tetris8.png"),
               pg.image.load("images/Tetris9.png")]
imageList = [pg.image.load("images/LightBlueBlock.png"), pg.image.load("images/GreenBlock.png"), pg.image.load("images/OrangeBlock.png"),
            pg.image.load("images/RedBlock.png"), pg.image.load("images/PurpleBlock.png"), pg.image.load("images/BlueBlock.png"),
            pg.image.load("images/YellowBlock.png")]
recordables = [level, lines, score]


def updateUI():
   for i in range(len(recordables)):
       for j in range(len(str(recordables[i]))):
           screen.blit(numberImages[(recordables[i] // 10 ** j) % 10], (800 - 60 - (25 * (j + 1)), 210 + (65 * i)))


def fillFutureGrid(letter):
   for x in range(4):
       futureGrid.append([])
       for y in range(6):
           futureGrid[x].append(letter)


def fillGrid(letter):
   for x in range(20):
       grid.append([])
       for y in range(10):
           grid[x].append(letter)


def resetFutureGrid():
   for x in range(4):
       for y in range(6):
           futureGrid[x][y] = "_"


futureGrid = []
fillFutureGrid("_")
grid = []
fillGrid("_")


def printGrid():
   for r in grid:
       for c in r:
           print(c, end="")
       print()


def getPos(character):
   position = []
   for r in range(20):
       for c in range(10):
           if grid[r][c] == character:
               position.append(r)
               position.append(c)
   return position


def getFuturePos(character):
   position = []
   for r in range(4):
       for c in range(6):
           if futureGrid[r][c] == character:
               position.append(r)
               position.append(c)
   return position


class Shape:
   def __init__(self, coordinates, color, blockRotateList, letter):
       self.coordinates = coordinates
       self.color = color
       self.blockRotateList = blockRotateList
       self.position = 0
       self.letter = letter

   def getCoordinates(self):
       return self.coordinates

   def placeFutureShape(self):
       for i in range(7):
           if i % 2 == 0:
               futureGrid[self.coordinates[i] + 1][self.coordinates[i + 1] - 2] = "X"
       screen.blit(pg.image.load("images/TetrisUi.png"), (0, 0))
       updateUI()

   def placeShape(self):
       global newCoords
       self.position = 0
       for i in range(7):
           if i % 2 == 0:
               grid[self.coordinates[i]][self.coordinates[i + 1]] = "U"
               newCoords[i] = self.coordinates[i]
               newCoords[i + 1] = self.coordinates[i + 1]
       screen.blit(pg.image.load("images/TetrisUi.png"), (0, 0))
       updateUI()

   def checkLoss(self):
       global gameOver
       global Loss
       for i in range(7):
           if i % 2 == 0:
               if not (grid[self.coordinates[i]][self.coordinates[i + 1]] == "_"):
                   Loss = True
                   gameOver = True

   def rotate(self, direction):
       global newCoords
       global canMove
       canMove = True
       if direction == -1:
           self.position = (self.position - 1) % (len(self.blockRotateList))
       for i in range(7):
           if i % 2 == 0:
               if (newCoords[i] + (self.blockRotateList[self.position][i] * direction) > 19) or (newCoords[i] + (self.blockRotateList[self.position][i] * direction) < 0):
                   canMove = False
               elif (newCoords[i + 1] + (self.blockRotateList[self.position][i + 1] * direction) > 9) or (newCoords[i + 1] + (self.blockRotateList[self.position][i + 1] * direction) < 0):
                   canMove = False
               elif grid[(newCoords[i]) + (self.blockRotateList[self.position][i] * direction)][newCoords[i + 1] + (self.blockRotateList[self.position][i + 1] * direction)] != "_" and grid[(newCoords[i]) + (self.blockRotateList[self.position][i] * direction)][newCoords[i + 1] + (self.blockRotateList[self.position][i + 1] * direction)] != "U":
                   canMove = False
       if canMove:
           #pg.mixer.Sound.play(turnSound)
           for i in range(7):
               if i % 2 == 0:
                   grid[newCoords[i]][newCoords[i + 1]] = "_"
           for i in range(7):
               if i % 2 == 0:
                   newCoords[i] += (self.blockRotateList[self.position][i] * direction)
                   newCoords[i + 1] += (self.blockRotateList[self.position][i + 1] * direction)
           for i in range(7):
               if i % 2 == 0:
                   grid[newCoords[i]][newCoords[i + 1]] = "U"
           if direction == 1:
               self.position = (self.position + 1) % (len(self.blockRotateList))
       else:
           if direction == -1:
               self.position = (self.position + 1) % (len(self.blockRotateList))

   def updatePlay(self):
       letterU = getPos("U")
       underscores = getPos("_")
       letterS = getPos("S")
       letterZ = getPos("Z")
       letterI = getPos("I")
       letterJ = getPos("J")
       letterL = getPos("L")
       letterO = getPos("O")
       letterT = getPos("T")

       updateLetter = [letterS, letterZ, letterI, letterO, letterJ, letterL, letterT]
       for i in range(len(underscores) - 1):
           if i % 2 == 0:
               pg.draw.rect(screen, BGCOLOR, (underscores[i + 1] * 30 + 100, underscores[i] * 30, 30, 30))
       for i in range(len(letterU) - 1):
           if i % 2 == 0:
               screen.blit(imageList[currentNumber], ((letterU[i + 1] * 30) + 100, (letterU[i] * 30)))
       for j in range(7):
           for i in range(len(updateLetter[j]) - 1):
               if i % 2 == 0:
                   screen.blit(imageList[j], ((updateLetter[j][i + 1] * 30) + 100, (updateLetter[j][i] * 30)))
       pg.display.update()

   def updateFuture(self):
       letterX = getFuturePos("X")
       funderscores = getFuturePos("_")
       for i in range(len(funderscores) - 1):
           if i % 2 == 0:
               pg.draw.rect(screen, BGCOLOR, (funderscores[i + 1] * 30 + 511, funderscores[i] * 30 + 61, 30, 30))
       for i in range(len(letterX) - 1):
           if i % 2 == 0:
               screen.blit(imageList[futureNumber], ((letterX[i + 1] * 30) + 511, (letterX[i] * 30) + 61))
       pg.display.update()


# rotatelists
oBlockRotate = [[0, 0, 0, 0, 0, 0, 0, 0]]
tBlockRotate = [[-1, 1, 0, 0, 1, -1, -1, -1], [1, 1, 0, 0, -1, -1, -1, 1], [1, -1, 0, 0, -1, 1, 1, 1],
               [-1, -1, 0, 0, 1, 1, 1, -1]]
zBlockRotate = [[-1, 2, 0, 1, -1, 0, 0, -1], [1, -2, 0, -1, 1, 0, 0, 1]]
sBlockRotate = [[-2, 1, -1, 0, 0, 1, 1, 0], [2, -1, 1, 0, 0, -1, -1, 0]]
lBlockRotate = [[-1, 1, 0, 0, 1, -1, -2, 0], [1, 1, 0, 0, -1, -1, 0, 2], [1, -1, 0, 0, -1, 1, 2, 0],
               [-1, -1, 0, 0, 1, 1, 0, -2]]
jBlockRotate = [[-1, 1, 0, 0, 1, -1, 0, -2], [1, 1, 0, 0, -1, -1, -2, 0], [1, -1, 0, 0, -1, 1, 0, 2],
               [-1, -1, 0, 0, 1, 1, 2, 0]]
iBlockRotate = [[-1, 1, 0, 0, 1, -1, 2, -2], [1, -1, 0, 0, -1, 1, -2, 2]]

letterList = ["S", "Z", "I", "O", "J", "L", "T"]

# original coords
oBlock = Shape([1, 4, 1, 5, 0, 4, 0, 5], RED, oBlockRotate, letterList[3])

tBlock = Shape([0, 3, 0, 4, 0, 5, 1, 4], YELLOW, tBlockRotate, letterList[6])

zBlock = Shape([0, 3, 0, 4, 1, 4, 1, 5], GREEN, zBlockRotate, letterList[1])

sBlock = Shape([1, 3, 1, 4, 0, 4, 0, 5], LIGHTBLUE, sBlockRotate, letterList[0])

lBlock = Shape([0, 3, 0, 4, 0, 5, 1, 3], BLUE, lBlockRotate, letterList[5])

jBlock = Shape([0, 3, 0, 4, 0, 5, 1, 5], PURPLE, jBlockRotate, letterList[4])

iBlock = Shape([0, 3, 0, 4, 0, 5, 0, 6], ORANGE, iBlockRotate, letterList[2])

blockList = [sBlock, zBlock, iBlock, oBlock, jBlock, lBlock, tBlock]


def validMove(r, c, letter):
   global newCoords
   canMove = True
   for i in range(7):
       if i % 2 == 0:
           if (newCoords[i] + r > 19):
               canMove = False
           elif (newCoords[i + 1] + c > 9) or (newCoords[i + 1] + c < 0):
               canMove = False
           elif grid[(newCoords[i]) + r][newCoords[i + 1]] != "_" and grid[(newCoords[i]) + r][
               newCoords[i + 1]] != "U":
               canMove = False
           elif grid[(newCoords[i])][newCoords[i + 1] + c] != "_" and grid[(newCoords[i])][
               newCoords[i + 1] + c] != "U":
               canMove = False
   return canMove


def hitBlock(r, c, letter):
   global newCoords
   hitBottom = False
   for i in range(7):
       if i % 2 == 0:
           if (newCoords[i] + r > 19):
               hitBottom = True
           elif grid[(newCoords[i]) + r][newCoords[i + 1]] != "_" and grid[(newCoords[i]) + r][
               newCoords[i + 1]] != "U":
               hitBottom = True
   return hitBottom


def moveShape(r, c, letter):
   global newCoords
   global rowHighlight
   global highlightTick
   if validMove(r, c, letter):
       for i in range(7):
           if i % 2 == 0:
               grid[newCoords[i]][newCoords[i + 1]] = "_"
       for i in range(7):
           if i % 2 == 0:
               grid[newCoords[i] + r][newCoords[i + 1] + c] = "U"
               newCoords[i] = newCoords[i] + r
               newCoords[i + 1] = newCoords[i + 1] + c
   elif hitBlock(r, c, letter):
       for i in range(7):
           if i % 2 == 0:
               grid[newCoords[i]][newCoords[i + 1]] = letter
       if rowHighlight == False:
           rowHighlight = True
           highlightTick = 0


def checkRow():
   rowList = []
   for r in range(20):
       counter = 0
       for c in range(10):
           if grid[r][c] != "_":
               counter += 1
           if counter == 10:
               rowList.append(r)
   return rowList

def highlightRow():
   global highlightTick
   global nextShape
   global rowHighlight
   global holdDown
   global holdLeft
   global holdRight
   if len(checkRow()) < 1:
       nextShape = True
       rowHighlight = False
   else:
       for i in range(len(checkRow())):
           if highlightTick == 5:
               nextShape = True
               rowHighlight = False
           elif highlightTick % 2 == 0:
               #pg.mixer.Sound.play(rowSound)
               screen.blit(pg.image.load("images/TetrisHighlight.png"),(100,checkRow()[i]*30))
               pg.display.update()
           elif highlightTick % 2 == 1:
               currentShape.updatePlay()
       highlightTick += 1


def clearRow():
   global fallSpeed
   global lines
   lineCounter = 0
   for r in range(20):
       counter = 0
       for c in range(10):
           if grid[r][c] != "_":
               counter += 1
           if counter == 10:
               for i in range(-r,1):
                   grid[abs(i)] = grid[abs(i) - 1]
               grid[0] = ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"]
               recordables[1] += 1
               recordables[0] = (recordables[1] // 10) + 1
               fallSpeed = 500 * (2 / (1 * recordables[0] + 1))
               lineCounter += 1
   # 40 * (n + 1) 100 * (n + 1)  300 * (n + 1)  1200 * (n + 1)
   if lineCounter == 0:
       timesBY = 0
   elif lineCounter == 1:
       timesBY = 40
   elif lineCounter == 2:
       timesBY = 100
   elif lineCounter == 3:
       timesBY = 300
   else:
       timesBY = 1200

   recordables[2] += timesBY * (recordables[0] + 1)
   updateUI()


def restartGame():
   global grid
   global futureGrid
   global Loss
   global rowHighlight
   global holdDown
   global holdLeft
   global holdRight
   global gameOver
   global nextShape
   global level
   global lines
   global score
   global fallTimer
   global fallSpeed
   global recordables
   global futureNumber
   global dGO

   grid = []
   futureGrid = []
   Loss = False
   rowHighlight = False
   holdDown = False
   holdLeft = False
   holdRight = False
   gameOver = False
   nextShape = True
   level = 1
   lines = 0
   score = 0
   recordables = [level,lines,score]
   fallTimer = 0
   fallSpeed = 500
   fillGrid("_")
   fillFutureGrid("_")
   screen.blit(pg.image.load("images/TetrisUi.png"), (0, 0))
   futureNumber = random.randint(0, 6)
   timer.tick()
   dGO = 0
   updateUI()
   pg.display.update()

timer.tick()
futureNumber = random.randint(0, 6)
while run:
   timer.tick()
   if not Loss:
       fallTimer += timer.get_rawtime()
       highlightTimer += timer.get_rawtime()
       if fallTimer > fallSpeed and not rowHighlight and not holdDown:
           moveShape(1, 0, letterList[currentNumber])
           fallTimer = 0
           currentShape.updatePlay()

       if rowHighlight:
           if highlightTimer > 100:
               highlightRow()
               highlightTimer = 0

       if nextShape:
           resetFutureGrid()
           fallTimer = 0
           clearRow()
           currentNumber = futureNumber
           currentShape = blockList[currentNumber]
           currentShape.checkLoss()
           currentShape.placeShape()
           futureNumber = random.randint(0, 6)
           futureShape = blockList[futureNumber]
           futureShape.placeFutureShape()
           currentShape.updatePlay()
           futureShape.updateFuture()
           nextShape = False

       for event in pg.event.get():
           if event.type == pg.QUIT:
               run = False

           if event.type == pg.KEYDOWN and not rowHighlight:
               if event.key == pg.K_LEFT:
                   moveShape(0, -1, letterList[currentNumber])
                   holdLeft = True
                   holdLeftTimer = 0
               if event.key == pg.K_RIGHT:
                   moveShape(0, 1, letterList[currentNumber])
                   holdRight = True
                   holdRightTimer = 0
               if event.key == pg.K_DOWN:
                   holdDown = True
                   holdDownTimer = 0
               elif event.key == pg.K_z:
                   currentShape.rotate(-1)
               elif event.key == pg.K_x:
                   currentShape.rotate(+1)
               elif event.key == pg.K_p:
                   Loss = True
                   gamePaused = True
               elif event.key == pg.K_r:
                   restartGame()
               currentShape.updatePlay()
           if event.type == pg.KEYUP:
               if event.key == pg.K_DOWN:
                   holdDown = False
                   holdDownTimer = 0
               if event.key == pg.K_LEFT:
                   holdLeft = False
                   holdLeftTimer = 0
               if event.key == pg.K_RIGHT:
                   holdRight = False
                   holdRightTimer = 0
       if not rowHighlight:
           if holdDown:
               holdDownTimer += timer.get_rawtime()
               if holdDownTimer > 50:
                   moveShape(1, 0, letterList[currentNumber])
                   holdDownTimer = 0
                   currentShape.updatePlay()
           if holdLeft:
               holdLeftTimer += timer.get_rawtime()
               if holdLeftTimer > 250:
                   moveShape(0, -1, letterList[currentNumber])
                   holdLeftTimer = 0
                   currentShape.updatePlay()
           if holdRight:
               holdRightTimer += timer.get_rawtime()
               if holdRightTimer > 250:
                   moveShape(0, 1, letterList[currentNumber])
                   holdRightTimer = 0
                   currentShape.updatePlay()
   else:
       if gameOver and dGO == 0:
           screen.blit(pg.image.load("images/TetrisGameOver.png"),(100,0))
           dGO += 1
       if gamePaused:
           screen.blit(pg.image.load("images/TetrisPaused.png"), (100, 0))
           gamePaused = False
       pg.display.update()

       for event in pg.event.get():
           if event.type == pg.QUIT:
               run = False

           if event.type == pg.KEYDOWN:
               if event.key == pg.K_r:
                   restartGame()
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_p:
                   if not gameOver:
                       Loss = not Loss
                       screen.blit(pg.image.load("images/TetrisUi.png"), (0, 0))
                       updateUI()
                       currentShape.updatePlay()
                       futureShape.updateFuture()
                       pg.display.update()
