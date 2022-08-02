# Imports
import curses
from curses import wrapper
import queue

# Maze to test path
maze = [
    ["/", "/", "/", "O", "/", "/", "/", "/", "/", "/"],  # O -> Start
    ["/", " ", " ", " ", " ", " ", " ", " ", " ", "/"],
    ["/", "/", " ", "/", "/", "/", "/", "/", " ", "/"],
    ["/", " ", " ", "/", " ", " ", " ", " ", " ", "/"],
    ["/", " ", "/", " ", " ", "/", " ", "/", "/", "/"],
    ["/", " ", " ", " ", " ", "/", " ", " ", " ", "/"],
    ["/", "/", "/", "/", "/", "/", "/", "/", "X", "/"],  # X -> Finish
]
START = "O"
END = "X"
OBSTICAL = "/"

def print_maze(maze, stdscr, path = []):
    GREEN = curses.color_pair(1)
    BLACK = curses.color_pair(2)
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path and maze[i][j] != START and maze[i][j] != END:
                stdscr.addstr(i, j*2 , "-", GREEN)
            else:
                stdscr.addstr(i, j*2, value, BLACK)

def start(maze):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == START:
                return i, j

def find_neighbours(maze, row, col):
    neighbours = []
    if row > 0:
        neighbours.append((row - 1, col))
    if row + 1 < len(maze):
        neighbours.append((row + 1, col))
    if col > 0:
        neighbours.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbours.append((row, col + 1))
    return neighbours

def search_path(maze, stdscr):
    start_pos = start(maze)
    path_queue = queue.Queue()          
    path_queue.put([start_pos])

    checked = set()
    while not path_queue.empty():
        path= path_queue.get()
        row, col = path[-1]              

        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()

        if maze[row][col] == END:
            stdscr.addstr("\nPress any key to end")
            return path

        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            new_row, new_col = neighbour
            if neighbour not in checked and maze[new_row][new_col] != OBSTICAL:
                new_path = path + [neighbour]
                path_queue.put((new_path))
                checked.add(neighbour)

    if path_queue.empty():
        stdscr.addstr("\nNo valid solution!")
        stdscr.addstr("\nPress any key to end")

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    search_path(maze, stdscr)
    stdscr.getch()

wrapper(main)

