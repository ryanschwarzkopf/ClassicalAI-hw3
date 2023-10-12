from collections import deque as queue

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
def DFS(graph, i, j, path, visited):
    if i < 0 or j < 0 or i >= len(graph) or j >= len(graph[0]): return
    if graph[i][j] == 'x' or (i,j) in visited: return
    if ((i,j) in visited): return
    if graph[i][j] == 'g':
        path.append((i,j))
        return path
    visited.add((i,j))
    print(visited)
    
    moves = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for ci, cj in moves:
        path.append((i,j))
        answer = DFS(graph,i+ci,j+cj, path, visited)
        if answer != None: return answer

def BFS(graph, i, j):
    vis = [[False for i in range(len(graph[0]))] for i in range(len(graph))]
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
            if(isValid(graph, vis, adjx, adjy,dRow[i], dCol[i])):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True
                if(graph[adjx][adjy] == "g"):
                    print("Found Goal!!\n")
                    return vis
    
    return vis

def isValid(graph, vis, row, col, dRow, dCol):
    if row < 0 or col < 0 or row >= len(graph) or col >= len(graph[0]):
        return False
    if (vis[row][col]):
        return False
    if(graph[row][col] == "x"): 
        return False

    return True

def Astar():
    pass

# distance between two points along axis
def M(x, y, gx, gy):
    return abs(gx - x) + abs(gy - y)

# euclidean distance between two points
def S(x, y, gx, gy):
    return (((gx - x)**2)+((gy - y)**2))**(0.5)

# minimum distance among x or y axis to goal
def HV(x, y, gx, gy):
    return min(abs(gx - x), abs(gy - y))

def print_output(vis):
    tmp = 0
    for row in vis:
        for cell in row:
            if(cell == False):
                tmp = 0
            else:
                tmp = 1
            
            print(tmp, end= " ")
        print()

def main():
    import sys
    import os

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
        path = DFS(world, start[0], start[1], [], set())
    elif method == 'BFS':
        path = BFS(world, start[0], start[1])
    
    print_output(path)

if __name__ == "__main__":
    main()

