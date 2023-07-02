import pygame
import math
from queue import PriorityQueue
import time

width = 800
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("Dijkstra's Path Finding Algorithm")

# Colors 
Default = (27, 26, 23) 
Grid = (50, 50, 50)
Start = (255, 165 ,0)
End = (64, 224, 208)

Closed = (34, 40, 49)
Open = (57, 62, 70)
Barrier = (230, 213, 184)
Path = (97, 115, 244)


class Tile:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = Default
        self.neighbors = []
    
    def getPos(self):
        return self.row, self.col
    
    def getState(self):
        return self.color
    
    def checkState(self, state):
        return self.color == state
    
    def updateState(self, state):
        self.color = state

    def reset(self):
        self.color = Default
    
    def draw(self , window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def updateNeighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].checkState(Barrier):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].checkState(Barrier):
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].checkState(Barrier):
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].checkState(Barrier):
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstructPath(prevTile, end, draw):
    while end in prevTile:
        end = prevTile[end]
        end.updateState(Path)
        draw()

def algorithm(draw, grid, start, end):

    cells = 0

    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))

    prevTile = {}

    gScore = {tile: float("inf") for row in grid for tile in row}
    gScore[start] = 0

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        cureentTile = openSet.get()[2]
        openSetHash.remove(cureentTile)

        if cureentTile == end:
            reconstructPath(prevTile, end, draw)
            end.updateState(End)
            start.updateState(Start)

            print("\n----------------------Path Found!----------------------")
            print("Cells Checked: ", cells)
            print("Path Length: ", gScore[end]+1)
            

            return True
        
        for neighbor in cureentTile.neighbors:
            tempGScore = gScore[cureentTile] + 1

            if tempGScore < gScore[neighbor]:

                prevTile[neighbor] = cureentTile

                gScore[neighbor] = tempGScore

                if neighbor not in openSetHash:
                    count += 1

                    openSet.put((gScore[neighbor], count, neighbor))

                    openSetHash.add(neighbor)

                    neighbor.updateState(Open)
        
        draw()
        
        if cureentTile != start:
            cureentTile.updateState(Closed)
            
    print("\n--------------------Path Not Found!--------------------")
    print("Cells Checked: ", cells)
    return False


def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap, rows)
            grid[i].append(tile)
    return grid
    
def drawGrid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, Grid, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, Grid, (j*gap, 0), (j*gap, width))


def draw(window, grid, rows, width):
    window.fill(Default)
    for row in grid:
        for tile in row:
            tile.draw(window)
    drawGrid(window, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y , x = pos
    row = y // gap
    col = x // gap
    return row , col

def main(window, width):
    ROWS = 25
    grid = makeGrid(ROWS, width)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(window, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos, ROWS, width)

                tile = grid[row][col]

                if not start and tile != end:
                    start = tile
                    start.updateState(Start)
                
                elif not end and tile != start:
                    end = tile
                    end.updateState(End)

                elif tile != start and tile != end:
                    tile.updateState(Barrier)
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos, ROWS, width)
                tile = grid[row][col]
                tile.reset()
                if tile == start:
                    start = None
                elif tile == end:
                    end = None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for tile in row:
                            tile.updateNeighbors(grid)
                    startTime = time.time()

                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                    endTime = time.time()
                    print("Time Taken : ",endTime - startTime)
                    print("-------------------------------------------------------")


                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)

    pygame.quit()
main(window, width)
    