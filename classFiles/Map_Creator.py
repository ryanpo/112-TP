from tkinter import *
import random
import copy

'''
Things to add:
1. direction depends on position, favouring branches, then increasing island removal
2. 8 starting points converging to the middle and normal walkers in the center
'''
def createList2(n):
    result = []
    for i in range(n):
        tmp = []
        for j in range(n):
            tmp += ["Z"]
        result += [tmp]
    return result

def tileHash(lst,row,col):
    result = set()
    if lst[row-1][col-1] != lst[row][col]:
        result.add(0)
    if lst[row-1][col] != lst[row][col]:
        result.add(1)
    if lst[row-1][col+1] != lst[row][col]:
        result.add(2)
    if lst[row][col-1] != lst[row][col]:
        result.add(3)
    if lst[row][col+1] != lst[row][col]:
        result.add(5)
    if lst[row+1][col-1] != lst[row][col]:
        result.add(6)
    if lst[row+1][col] != lst[row][col]:
        result.add(7)
    if lst[row+1][col+1] != lst[row][col]:
        result.add(8)
    return result

def drunkWalk(lst,n,startRow,startCol,branching = 10000):
    steps = []
    seen = set()
    row = startRow
    col = startCol
    walkers = [(row,col)]
    lst[startRow-1][startCol] = "A"
    lst[startRow+1][startCol] = "A"
    lst[startRow-1][startCol-1] = "A"
    lst[startRow][startCol-1] = "A"
    lst[startRow][startCol+1] = "A"
    lst[startRow+1][startCol+1] = "A"
    lst[startRow+1][startCol-1] = "A"
    lst[startRow-1][startCol+1] = "A"
    steps.append(copy.deepcopy(lst))
    while len(seen) <= n:
        if random.randint(1,branching) == 2 and len(walkers) > 1:
            walkers.remove(walkers[random.randint(1,len(walkers)-1)])
        for k in range(len(walkers)):
            seen.add(walkers[k])
            lst[walkers[k][0]][walkers[k][1]] = "A"
            steps.append(copy.deepcopy(lst))
            dCol, dRow = random.choice([[1,0],[-1,0],[0,1],[0,-1]])
            walkers[k] = (walkers[k][0]+dRow, walkers[k][1]+dCol)
            if random.randint(1,len(seen)*2) == 1:
                walkers.append((random.choice(list(seen))))
    # for i in range(len(lst)):
    #     for j in range(len(lst[0])):
    #         if (i,j) in seen:
    #             lst[i][j] = "A"
    return (lst, steps)

def removeIslands(lst):
    for i in range(1,len(lst)-1):
        for j in range(1,len(lst[0])-1):
            if lst[i][j] == "A":
                s = tileHash(lst,i,j)
                if (0 not in s) and (1 in s) and (3 in s):
                    lst[i][j] = "Z"
                if (2 not in s) and (1 in s) and (5 in s):
                    lst[i][j] = "Z"
                if (6 not in s) and (3 in s) and (7 in s):
                    lst[i][j] = "Z"
                if (8 not in s) and (5 in s) and (7 in s):
                    lst[i][j] = "Z"
    return lst


def magnify(lst):
    result = createList2(len(lst)*3)
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            result[i*3][j*3] = lst[i][j]
            result[i*3+1][j*3+1] = lst[i][j]
            result[i*3][j*3+1] = lst[i][j]
            result[i*3+1][j*3] = lst[i][j]
            result[i*3+2][j*3] = lst[i][j]
            result[i*3+2][j*3+1] = lst[i][j]
            result[i*3+2][j*3+2] = lst[i][j]
            result[i*3+1][j*3+2] = lst[i][j]
            result[i*3][j*3+2] = lst[i][j]
    return result

def tiling(lst):
    result = copy.deepcopy(lst)
    for row in range(1,len(lst)-1):
        for col in range(1,len(lst[0])-1):
            if lst[row][col] == "Z":
            ### Corners ###
                if tileHash(lst,row,col) == {0}:
                    result[row][col] = "BOT RIGHT C"
                elif tileHash(lst,row,col) == {2}:
                    result[row][col] = "BOT LEFT C"
                elif tileHash(lst,row,col) == {6}:
                    result[row][col] = "TOP RIGHT C"
                elif tileHash(lst,row,col) == {8}:
                    result[row][col] = "TOP LEFT C"
            ### Walls ###
                elif tileHash(lst,row,col) in [{0,3,6},{0,3},{3,6}]:
                    result[row][col] = "RIGHT WALL"
                elif tileHash(lst,row,col) in [{2,5,8},{2,5},{5,8}]:
                    result[row][col] = "LEFT WALL"
                elif tileHash(lst,row,col) in [{0,1,2},{0,1},{1,2}]:
                    result[row][col] = "BOT WALL"
                    result[row+1][col] = "BOT WALL S"
                elif tileHash(lst,row,col) in [{6,7,8},{6,7},{7,8}]:
                    result[row][col] = "TOP WALL"
            ### In-Corners ###
                elif tileHash(lst,row,col) == {0,1,2,5,8}:
                    result[row][col] = "TOP RIGHT IN C"
                elif tileHash(lst,row,col) == {0,1,2,3,6}:
                    result[row][col] = "TOP LEFT IN C"
                elif tileHash(lst,row,col) == {0,3,6,7,8}:
                    result[row][col] = "BOT LEFT IN C"
                elif tileHash(lst,row,col) == {2,5,6,7,8}:
                    result[row][col] = "BOT RIGHT IN C"
            if lst[row][col] == "A":
            ### Top Flats ###
                if tileHash(lst,row,col) in [{0,1,2},{0,1,2,5,8},{0,1}]:
                    result[row][col] = "TOP FLAT"
                elif tileHash(lst,row,col) in [{0,1,2,3,6},{1,2}]:
                    result[row][col] = "TOP FLAT S"
    return result




# Updated Animation Starter Code

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.walk = drunkWalk(createList2(50),100,25,25)
    data.map = data.walk[0]
    data.steps = data.walk[1]
    data.count = 0
    data.start = False
    pass

def mousePressed(event, data):
    data.start = True
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    if data.start and data.count < len(data.steps)-1:
        data.count += 1
    pass

def redrawAll(canvas, data):
    for row in range(len(data.map)):
        for col in range(len(data.map[0])):
            if data.steps[data.count//1][row][col] == "A":
                canvas.create_rectangle(col*10,row*10,col*10+10,row*10+10,fill = "Black")
    pass

####################################
# use the run function as-is
####################################

def run(width=500, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(500, 500)