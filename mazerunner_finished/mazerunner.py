import queue
import pygame as py
import time
WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,100)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WIDTH, HEIGHT = 800, 800

TILE=(50,50)

LOADPIC= py.image.load('maze_rs/load.png')
LOADPIC= py.transform.scale(LOADPIC,TILE)
PATH= py.image.load('maze_rs/path.png')
PATH= py.transform.scale(PATH,TILE)
WALLImg= py.image.load('maze_rs/wall.png')
WALLImg= py.transform.scale(WALLImg,TILE)
PATHImg= py.image.load('maze_rs/emptypiece.png')
PATHImg= py.transform.scale(PATHImg,TILE)
STARTImg= py.image.load('maze_rs/red_flag.png')
STARTImg= py.transform.scale(STARTImg,TILE)
STOPImg= py.image.load('maze_rs/bomb.png')
STOPImg= py.transform.scale(STOPImg,TILE)

py.init()
py.display.set_caption("Mazerunner")
WIN=py.display.set_mode((WIDTH,HEIGHT))

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", "O", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "X", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#", " ", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

class Spot:
    def __init__(self,row,col):
        self.x=self.col=col
        self.y=self.row=row
        self.wall=False
        self.end=False
        self.start=False
        self.pos=(row,col)
        self.path=[]
    def is_barrier(self):
        if self.wall==True:
            return True
        else:
            return False
    def FindNeighbour(self,grid,total_rows):
        self.neighbors = []
        if self.row < total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
    def draw(self,pic=None):
        if pic != None:
            WIN.blit(pic,(self.x*50,self.y*50))
        elif self.wall==True:
            WIN.blit(WALLImg,(self.x*50,self.y*50))
        elif self.start==True:
            WIN.blit(STARTImg,(self.x*50,self.y*50))
        elif self.end==True:
            WIN.blit(STOPImg,(self.x*50,self.y*50))
        else:
            WIN.blit(PATHImg,(self.x*50,self.y*50))
def defineSpot(grid):
    for row in range(16):
        for col in range(16):
            if grid[row][col]=='#':
                grid[row][col]=Spot(row,col)
                grid[row][col].wall=True
            if grid[row][col]==' ':
                grid[row][col]=Spot(row,col)
            if grid[row][col]=='O':
                grid[row][col]=Spot(row,col)
                grid[row][col].start=True
            if grid[row][col]=='X':
                grid[row][col]=Spot(row,col)
                grid[row][col].end=True

def thuattoan(start_pos,end_pos):
    q=queue.Queue()
    q.put(start_pos)
    visited=set()
    while not q.empty():
        spot=q.get()
        for i in visited:
            if i.end==False and i.start == False:
                i.draw(LOADPIC)
            pass
        if spot == end_pos:
            return spot
            
        for neighbor in spot.neighbors:
            if neighbor in visited:
                continue
            
            if neighbor.wall==True:
                continue
            
            spot.path + [neighbor]
            neighbor.path=spot.path + [neighbor]
            q.put(neighbor)
            visited.add(neighbor)
def main():
    finish=False
    running=True
    FPS=10
    clock=py.time.Clock()
    defineSpot(maze)
    for row in range(16):
        for col in range(16):
            maze[row][col].FindNeighbour(maze,16)
            if maze[row][col].start==True:
                start_pos=maze[row][col]
                start_pos.path.append(start_pos)
                
    for row in range(16):
        for col in range(16):            
            if maze[row][col].end==True:
                end_pos=maze[row][col]
    
    q=queue.Queue()
    q.put(start_pos)
    visited=set()
    while running:
        WIN.fill(BLACK)
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                running=False
        
        for row in range(16):
            for col in range(16):
                maze[row][col].draw()
        
        if not q.empty() and finish == False:
            spot=q.get()
            for i in visited:
                if i.end==False and i.start == False:
                    i.draw(LOADPIC)
            if spot == end_pos:
                end = spot
                finish=True
            for neighbor in spot.neighbors:
                if neighbor in visited:
                    continue
                if neighbor.wall==True:
                    continue
                spot.path + [neighbor]
                neighbor.path=spot.path + [neighbor]
                q.put(neighbor)
                visited.add(neighbor)
        try:
            for i in end.path:
                if i.end==False and i.start == False:
                    i.draw(PATH)
        except:
            pass
        py.display.flip()
    
    py.quit()

main()