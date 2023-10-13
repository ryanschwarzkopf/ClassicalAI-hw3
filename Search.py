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
def DFS(graph, at, path, visited):
    i, j = at[0], at[1]
    
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
        if((newi,newj) not in visited) and newi >= 0 and newj >= 0 and newi < len(graph) and newj < len(graph[0]) and graph[newi][newj] != 'x':
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
1. Start with a tree that contains only the start state
2. Pick a fringe node n with the smallest heuristic.
3. If fringe node n represents a goal, then stop
4. Expand fringe node n
5. Go to 2
(All actions have the same cost, so we can prioritize based on only the heuristic)
'''
def Astar(world, start, goal, visited):
    pass

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
    path = ''           # path to gridworld file
    method = 'Astar'       # Default to A* search
    heur = 'S'      # Default to Straight-line heuristic

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-i':
            path = os.path.abspath(sys.argv[i+1])
        if sys.argv[i] == '-a':
            method = sys.argv[i+1]
        if sys.argv[i] == '-h':
            heur = sys.argv[i+1]
    if path == '':
        exit(1)

    fp = open(path, 'r', encoding='utf-8')
    lines = fp.readlines()
    fp.close()
    width = int(lines[0])
    height = int(lines[1])
    # delete the first two lines of the file with the width and height specifiers
    del lines[0]
    del lines[0]

    start, goal, world = build(lines)

    if method == 'Astar':
        path = Astar(world, start[0], start[1], goal[0], goal[1], heur)
    elif method == 'DFS':
        path = DFS(world, start, [], set())
    elif method == 'BFS':
        path = BFS(world, start[0], start[1])
    
    if path == None: print('No path found.')
    else:
        print(f'A* search: Cost={len(path)}. Heuristic={heur} \n', path) if method == 'Astar' else print(f'{method} search: Cost={len(path)} \n', path)

if __name__ == "__main__":
    main()

