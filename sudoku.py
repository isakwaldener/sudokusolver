import random
import pygame
from pygame.locals import *
pygame.init()


def main(gui):
    gui = gui()
    gui.game.createGame()
    gui.updateGame()
    gameOver = 0
    while(not gameOver):
        # checks for events
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type is QUIT:
                gameOver = 1
            elif event.type is MOUSEBUTTONDOWN:
                # click with mouse to choose where to add number
                pos = pygame.mouse.get_pos()
                point = (pos[1] / 50, pos[0] / 50)
                gui.game.userAddedNumber(point)
            elif keys[pygame.K_SPACE]:
                # click Space to solve
                gui.game.board.removeUserInput()
                if gui.game.board.solve():
                    gameOver = 1
        gui.updateGame()
    gui.game.board.printBoard()


class board():

    def __init__(self):
        # Initiate the board
        self._board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self._points = [(y, x) for y in range(9) for x in range(9)]

    def clear(self):
        for i in self._board:
            for j in self._board:
                self._board[i][j] = 0

    def getboard(self):
        return self._board

    def findNextPos(self):
        # Find next point that is 0
        for i in range(9):
            for j in range(9):
                if self._board[i][j] == 0:
                    return (i, j)
        return None

    def checkCol(self, col, number):
        # checks if number is in col
        for i in range(9):
            if abs(self._board[i][col]) == number:
                return False
        return True

    def checkRow(self, row, number):
        # checks if number is in row
        for i in range(9):
            if abs(self._board[row][i]) == number:
                return False
        return True

    def checkCube(self, row, col, number):
        # checks if number is in cube
        for i in range((row // 3) * 3, (row // 3) * 3 + 3):
            for j in range((col // 3) * 3, (col // 3) * 3 + 3):
                if abs(self._board[i][j]) == number:
                    return False
        return True

    def checkPoint(self, point, number):
        # checks if a numer is valid at a point
        rowOk = self.checkRow(point[0], number)
        colOk = self.checkCol(point[1], number)
        cubeOk = self.checkCube(point[0], point[1], number)
        if rowOk and colOk and cubeOk:
            return True
        else:
            return False

    def findCandidates(self, point):
        # find the numbers that are valid at the point
        candidates = []
        for i in range(1, 10):
            if self.checkPoint(point, i):
                candidates.append(i)
        return candidates

    def addNumber(self, point, num):
        self._board[point[0]][point[1]] = num

    def getNumber(self, point):
        return self._board[point[0]][point[1]]

    def removeUserInput(self):
        # return board to starting layout to solve it
        for point in self._points:
            if self.getNumber(point) > 0:
                self.addNumber(point, 0)

    def solve(self, test=False):
        # solves the board recursivley
        point = self.findNextPos()
        if not point:
            return True

        for i in range(1, 10):
            if self.checkPoint(point, i):
                self.addNumber(point, i)

                if self.solve(test):
                    if test:
                        self.addNumber(point, 0)
                    return True
                else:
                    self.addNumber(point, 0)
        return False

    def startBoard(self):
        # add startnumbers by check if the board is solveable for the number
        numbersAtStart = 18

        random.shuffle(self._points)

        for n, point in enumerate(self._points):
            if(n == numbersAtStart):
                break

            for i in self.findCandidates(point):
                if self.getNumber(point) == 0:
                    self.addNumber(point, i)

                if self.solve(True):
                    break

    def lockStartNumbers(self):
        # changes the numbers to negative so they can't be changed
        for i in range(9):
            for j in range(9):
                self._board[i][j] *= -1

    def printBoard(self):
        for i in range(9):
            print(self._board[i])

    def getPoints(self):
        return self._points


class game():

    def __init__(self):
        self.board = board()

    def createGame(self):
        self.board.startBoard()
        self.board.lockStartNumbers()

    def getBoardPoints(self):
        return self.board.getPoints()

    def getGameBoard(self):
        return self.board

    def gameOver(self, over=False):
        if over:
            return True

    def userAddedNumber(self, point):
        # checks keys to add number at point
        if self.board.getNumber(point) < 0:
            return None
        nokey = 1
        while(nokey):
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if keys[pygame.K_1]:
                    self.board.addNumber(point, 1)
                    nokey = 0
                if keys[pygame.K_2]:
                    self.board.addNumber(point, 2)
                    nokey = 0
                if keys[pygame.K_3]:
                    self.board.addNumber(point, 3)
                    nokey = 0
                if keys[pygame.K_4]:
                    self.board.addNumber(point, 4)
                    nokey = 0
                if keys[pygame.K_5]:
                    self.board.addNumber(point, 5)
                    nokey = 0
                if keys[pygame.K_6]:
                    self.board.addNumber(point, 6)
                    nokey = 0
                if keys[pygame.K_7]:
                    self.board.addNumber(point, 7)
                    nokey = 0
                if keys[pygame.K_8]:
                    self.board.addNumber(point, 8)
                    nokey = 0
                if keys[pygame.K_9]:
                    self.board.addNumber(point, 9)
                    nokey = 0


class gui():

    def __init__(self):
        self.game = game()
        self.disp = pygame.display.set_mode((450, 450))
        self.board = self.boardinit()
        self.gameBoard = self.game.getGameBoard()

    def boardinit(self):
        # creates a white background with lines to creat boxes
        background = pygame.Surface(self.disp.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        for i in range(9):
            vstartpos = (self.disp.get_height()/9 * i, 0)
            vendpos = (self.disp.get_width()/9*i, self.disp.get_width())
            hstartpos = (0, self.disp.get_height()/9 * i,)
            hendpos = (self.disp.get_width(), self.disp.get_width()/9*i)
            pygame.draw.line(background, (0, 0, 0), vstartpos, vendpos, 1)
            pygame.draw.line(background, (0, 0, 0), hstartpos, hendpos, 1)
        return background

    def updateGame(self):

        self.drawBoard()
        self.disp.blit(self.board, (0, 0))
        pygame.display.flip()

    def reDrawBackground(self):
        # redraws background and lines
        self.board.fill((250, 250, 250))
        for i in range(9):
            vstartpos = (self.disp.get_height()/9 * i, 0)
            vendpos = (self.disp.get_width()/9*i, self.disp.get_width())
            hstartpos = (0, self.disp.get_height()/9 * i,)
            hendpos = (self.disp.get_width(), self.disp.get_width()/9*i)
            pygame.draw.line(self.board, (0, 0, 0), vstartpos, vendpos, 1)
            pygame.draw.line(self.board, (0, 0, 0), hstartpos, hendpos, 1)

    def drawBoard(self):
        # Add numbers to the board
        font = pygame.font.Font(None, 30)
        self.reDrawBackground()

        for i in range(9):
            for j in range(9):
                num = abs(self.gameBoard.getNumber((i, j)))
                text = font.render('{0}'.format(num), 1, (0, 0, 0))
                self.board.blit(text, (j*50+20, i*50+20))


if __name__ == "__main__":
    main(gui)
