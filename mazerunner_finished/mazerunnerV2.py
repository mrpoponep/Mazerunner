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

TILE=(25,25)

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
            self.colli = WIN.blit(pic,(self.x*25,self.y*25))
        elif self.wall==True:
            self.colli = WIN.blit(WALLImg,(self.x*25,self.y*25))
        elif self.start==True:
            self.colli = WIN.blit(STARTImg,(self.x*25,self.y*25))
        elif self.end==True:
            self.colli = WIN.blit(STOPImg,(self.x*25,self.y*25))
        else:
            self.colli = WIN.blit(PATHImg,(self.x*25,self.y*25))

def initspot(maze):
    for row in range(32):
        r=[]
        for col in range(32):
            spot=Spot(row,col)
            r.append(spot)
        maze.append(r)

def main():
    maze=[]
    running=True
    finish = False
    FPS=15
    start_pos=None
    end_pos=None
    clock=py.time.Clock()
    start=False
    q=queue.Queue()
    initspot(maze)
    for row in range(32):
        for col in range(32):
            maze[row][col].FindNeighbour(maze,32)
            if maze[row][col].start==True:
                start_pos=maze[row][col]
                start_pos.path.append(start_pos)
                
    for row in range(16):
        for col in range(16):            
            if maze[row][col].end==True:
                end_pos=maze[row][col]
    
    while running:
        WIN.fill(BLACK)
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                running=False
            elif (event.type == py.MOUSEBUTTONDOWN) and start==False:
                mouse_pos = py.mouse.get_pos()
                mouse_buttons = py.mouse.get_pressed()
                for r in maze:
                    for spot in r:
                        if ( spot.colli.collidepoint(mouse_pos) ) and mouse_buttons[0]:
                            if spot.wall==False and spot.start==False and spot.end==False:
                                spot.wall=True
                            elif spot.wall==True:
                                spot.wall=False
                            elif spot.start==True:
                                spot.start=False
                                start_pos=None
                            elif spot.end==True:
                                spot.end=False
                                end_pos=None
                        if ( spot.colli.collidepoint(mouse_pos) ) and mouse_buttons[2]:
                            if start_pos==None and spot.wall==False:
                                spot.start=True
                                start_pos=spot
                                print('start')
                                print(start_pos)
                            elif start_pos != None and end_pos==None and spot.start==False and spot.wall==False:
                                spot.end=True
                                end_pos=spot
                                print('end')
                                print(end_pos)
            elif event.type == py.KEYDOWN and end_pos != None and start_pos != None:
                    if event.key == py.K_SPACE:    
                        q.put(start_pos)
                        visited=set()
                        start=True
            if event.type == py.KEYDOWN and finish==True and start==True:
                if event.key == py.K_ESCAPE:
                    maze=[]
                    initspot(maze)
                    q=queue.Queue()
                    start_pos=None
                    end_pos=None
                    finish=False
                    start=False
                    finalpath=None
                    visited.clear()
                if event.key == py.K_SPACE and finish==True and start==True:
                    finish=False
                    start=False
                    visited.clear()
                    q=queue.Queue()
                    finalpath=None

        for row in range(32):
            for col in range(32):
                maze[row][col].draw()

        if not q.empty() and finish==False and start==True:
            spot=q.get()
            for i in visited:
                if i.end==False and i.start == False:
                    i.draw(LOADPIC)
                pass
            if spot == end_pos:
                finalpath = spot
                finish=True
            for neighbor in spot.neighbors:
                if neighbor in visited:
                    continue

                if neighbor.wall==True:
                    continue
                
                neighbor.path=spot.path + [neighbor]
                q.put(neighbor)
                visited.add(neighbor)
        try:
            for i in finalpath.path:
                if i.end==False and i.start == False:
                    i.draw(PATH)
        except:
            pass
        

        py.display.flip()
    
    py.quit()

main()