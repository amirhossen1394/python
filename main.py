import curses


var = -CursesWindow

stack: _CursesWindow = curses.initscr()
curses.noecho()
curses.cbreak()
stack.keypad(True)


maxl = curses.LINES -1
maxc = curses.COLS -1

world = []

def init():

for i in range(maxl):
    world.append([])

    for j in range(maxc):
        world[i].append('.')

        def draw():
for i in range(maxl):
for j in range(maxc):
stack.addch( i, j, world[i][j])
stack.refresh()

init()
draw()


stack.refresh()
stack.getkey()
