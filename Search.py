'''
    Ryan Schwarzkopf
    Alfredo Gutierrez
    Oct 12, 2023
    
    The following is a description of the gridworld environment that your robot
    will interact with. Consider a NxM matrix gridworld. Cells are either blocked
    or unblocked. Blocked cells are marked as 'x'. Unblocked cells are marked as '_'
    The start cell is denoted by 's' and the goal cell is denoted by 'g'.
    
    The robot can only move to one of the eight adjacent cells (i.e., the cells to
    the north, northeast, east, southeast, south, southwest, west, and northwest
    of the current cell). The exception is if the cell or the path to the cell is
    blocked (a move to the northwest is invalid if both the north and the west
    cells are blocked; even if the northwest cell is free). The game character then
    seeks to determine the shortest unblocked path from its current cell to the goal
    cell.
    
    Algorithms DFS, BFS, and A* are the algorithms used to find the path to the goal.
    A* uses one of three heuristics: Euclidean distance, manhattan distance, or
    chebyshev distance.
    
    Any text file can by used as a grid world. The first line must contain only the
    number of rows (i.e. 5). The second line must contain the number of columns. 
    The next lines are row wise with nodes separated by spaces. The gridworld must
    have only one starting node and only one goal.
    
    Ex:
    4
    5
    _ s _ _	_
    x x x x	_
    _ x x x	_
    _ _ g _ _
	
    Please use this format for running the module:
    Search.py -i <inputfile> -a BFS|DFS|Astar -h M|S|HV
    
    The default algorithm is A* and the default heuristic is chebyshev(HV)
    DFS and BFS do not use any heuristic.
    The module returns: if the path was found, algorithm used, the total cost,
    and the path
'''

import sys
import os
from collections import deque as queue
import heapq

def build(lines):
    world = []
    start = []
    goal = []
    lineno = 0
    for line in lines:
        line = line.replace('\n', '')
        line = line.rstrip('\t')
        line = line.replace('\t', ' ')
        
        vals = line.split(' ')
        for i, val in enumerate(vals):
            if val == 's':
                start = [lineno, i]
            if val == 'g':
                goal = [lineno, i]
        if line != '':
            world.append(line.split(' '))
        lineno+=1
    return start, goal, world

'''
    dfs to each node
'''
def DFS(graph, start, path, visited):
    i, j = start[0], start[1]
    path.append((i,j))
    visited.add((i,j))
    if graph[i][j] == 'g':
        return path
    
    moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    if i > 0 and graph[i-1][j] != 'x':
        if j > 0 and graph[i][j-1] != 'x': moves.append((-1, -1))
        if j < len(graph[0])-1 and graph[i][j+1] != 'x': moves.append((-1, 1))
    if i < len(graph)-1 and graph[i+1][j] != 'x':
        if j > 0 and graph[i][j-1] != 'x': moves.append((1, -1))
        if j < len(graph[0])-1 and graph[i][j+1] != 'x': moves.append((1, 1))
        
    for ci, cj in moves:
        newi=i+ci
        newj=j+cj
        if((newi,newj) not in visited) and node_isValid(graph, (newi, newj)):
            answer = DFS(graph,[newi,newj], path, visited)
            if answer != None:
                return answer
    path.pop()
    return None
        
'''
    bfs to each node
'''
def BFS(graph, i, j):
    vis = [[False for i in range(len(graph[0]))] for i in range(len(graph))]
    parent = [[None for _ in range(len(graph[0]))] for _ in range(len(graph))]
    dRow = [0, -1, 0, 1, -1, -1, 1, 1]
    dCol = [-1, 0, 1, 0, -1, 1, -1, 1]
    
    q = queue()
    
    'Row i, j column'
    q.append((i, j))
    
    vis[i][j] = True
    
    while(len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        
        for i in range(8):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if(isValid(graph, vis, adjx, adjy,(x - dRow[i]),(y - dCol[i]), dRow[i], dCol[i])):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True
                parent[adjx][adjy] = (x, y)
                if(graph[adjx][adjy] == "g"):
                    return backtrack(parent, (i,j), (adjx, adjy))
    return None

# Check if the current cell is a valid move
def isValid(graph, vis, row, col, nRow, nCol, x, y):
    if row < 0 or col < 0 or row >= len(graph) or col >= len(graph[0]):
        return False
    if (vis[row][col]):
        return False
    if(graph[row][col] == "x"): 
        return False
    
    #When moving diagonal we check if the path to it is not blocked 
    if(x != 0 and y != 0):
        if nRow < 0 or nCol < 0 or nRow >= len(graph) or nCol >= len(graph[0]):
            return False
        if(vis[nRow + x ][nCol] and vis[nRow][nCol + y]):
            return False   
    return True

'''
    Check if any node is a valid node:
    (1) Node is on the graph.
    (2) Node is not on an X
'''
def node_isValid(graph, node):
    i, j = node[0], node[1]
    if i >= 0 and j >= 0 and i < len(graph) and j < len(graph[0]) and graph[i][j] != 'x':
        return True
    return False

'''
    Starting with goal node, add to path and find previously visited node in dictionary
'''
def reconstruct_path(came_from, node, start):
        path = [node]
        i, j = node[0], node[1]
        temp = f'{i}, {j}'
        while temp in came_from:
            node = came_from[temp]
            temp = f'{node[0]}, {node[1]}'
            path.append(node)
        path.reverse()
        return path

'''
1. Start with a tree that contains only the start state
2. Pick a fringe node n with the smallest heuristic.
3. If fringe node n represents a goal, then stop
4. Expand fringe node n
5. Go to 2
(All actions have the same cost, so we can prioritize based on only the heuristic)
'''
def Astar(graph, start, goal, heur):
    open, closed, open_set = [], [], []
    heapq.heappush(open, (0, (start[0],start[1])))
    open_set.append((start[0],start[1]))
    
    came_from = {}
    g_score = {f'{i}, {j}': float('inf') for i in range(len(graph)) for j in range(len(graph[0]))}
    g_score[f'{start[0]}, {start[1]}'] = 0
    f_score = {f'{i}, {j}': float('inf') for i in range(len(graph)) for j in range(len(graph[0]))}
    f_score[f'{start[0]}, {start[1]}'] = getHeur(heur,start[0],start[1],goal[0],goal[1])
    
    while open:
        junk, node = heapq.heappop(open)
        open_set.remove(node)
        closed.append(node)
        i, j = node[0], node[1]
        if graph[i][j] == 'g':
            return reconstruct_path(came_from, node, start)

        # Add all possible nodes based on its neighbors
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        if i > 0 and graph[i-1][j] != 'x':
            if j > 0 and graph[i][j-1] != 'x': moves.append((-1, -1))
            if j < len(graph[0])-1 and graph[i][j+1] != 'x': moves.append((-1, 1))
        if i < len(graph)-1 and graph[i+1][j] != 'x':
            if j > 0 and graph[i][j-1] != 'x': moves.append((1, -1))
            if j < len(graph[0])-1 and graph[i][j+1] != 'x': moves.append((1, 1))
            
        for ci, cj in moves:
            neighbor = (i+ci, j+cj)
            
            # check if the move is on the board, not on a wall, and not already visited
            if node_isValid(graph, neighbor) and neighbor not in closed:
                tentative_g_score = g_score[f'{i}, {j}'] + 1
                if tentative_g_score < g_score[f'{neighbor[0]}, {neighbor[1]}'] or neighbor not in open_set:
                    came_from[f'{neighbor[0]}, {neighbor[1]}'] = node
                    g_score[f'{neighbor[0]}, {neighbor[1]}'] = tentative_g_score
                    f_score[f'{neighbor[0]}, {neighbor[1]}'] = tentative_g_score + getHeur(heur, neighbor[0], neighbor[1], goal[0], goal[1])
                    if neighbor not in open:
                        heapq.heappush(open, (f_score[f'{neighbor[0]}, {neighbor[1]}'], neighbor))
                        open_set.append(neighbor)
    return None

#Saves a found path
def backtrack(parent, start, end):
    x = end[0]
    y = end[1]
    path = []
    while (x,y) != start:
        path.append((x,y))
        if parent[x][y] is not None:
            x, y = parent[x][y]
        else:
            break
    path.reverse()
    return path


def getHeur(heur, x, y, gx, gy):
    # manhattan distance: distance between two points along axis
    if heur == 'M':
        return abs(gx - x) + abs(gy - y)
    # euclidean distance between two points
    elif heur == 'S':
        return (((gx - x)**2)+((gy - y)**2))**(0.5)
    # chebyshev is max distance among an axis
    elif heur == 'HV':
        return max(abs(gx - x), abs(gy - y))


def main():
    # path = ''           # path to gridworld file
    # method = 'Astar'       # Default to A* search
    # heur = 'HV'      # Default to chebyshev heuristic

    '''
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-i':
            path = os.path.abspath(sys.argv[i+1])
        if sys.argv[i] == '-a':
            method = sys.argv[i+1]
        if sys.argv[i] == '-h':
            heur = sys.argv[i+1]
    if path == '':
        exit(1)
    '''
    sys.setrecursionlimit(10**6)
    f = open("answers.txt", "a")
    methods = ['DFS', 'BFS', 'Astar']
    heuristics = ['S', 'M', 'HV']
    for i in range(18):
        path = f'./inputs/{i+1}.txt'
        fp = open(path, 'r', encoding='utf-8')
        lines = fp.readlines()
        fp.close()
        width = int(lines[0])
        height = int(lines[1])
        # delete the first two lines of the file with the width and height specifiers
        del lines[0]
        del lines[0]

        start, goal, world = build(lines)
        f.write(f'Input file: {i+1} \n')
        for method in methods:
            if method == 'Astar':
                for heur in heuristics:
                    path = Astar(world, start, goal, heur)
                    if path == None: f.write(f'Astar, {heur}, No path found \n')
                    else: f.write(f'Astar, {heur}, Cost={len(path)} \n')
            elif method == 'DFS':
                path = DFS(world, start, [], set())
                if path == None: f.write(f'DFS, No path found')
                else: f.write(f'DFS, Cost={len(path)}')
            elif method == 'BFS':
                path = BFS(world, start[0], start[1])
                if path == None: f.write(f'BFS, No path found')
                else: f.write(f'BFS, Cost={len(path)}')
            f.write('\n')
    f.close()

    '''
    if path == None: print('No path found.')
    else:
        print(f'A* search: Cost={len(path)}. Heuristic={heur} \n', path) if method == 'Astar' else print(f'{method} search: Cost={len(path)} \n', path)
    '''
    
if __name__ == "__main__":
    main()

