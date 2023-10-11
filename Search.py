
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

def BFS():
    pass

'''
    dfs to each node
'''
def DFS(graph, i, j):
    if i < 0 or j < 0 or i >= len(graph) or j >= len(graph[0]): return
    if graph[i][j] != '-': return
    graph[i][j] = 0 # set to 0 if visited so we don't go back.
    DFS(graph,i-1,j-1)
    DFS(graph,i,j-1)
    DFS(graph,i+1,j-1)
    DFS(graph,i-1,j)
    DFS(graph,i+1,j)
    DFS(graph,i-1,j+1)
    DFS(graph,i,j+1)
    DFS(graph,i+1,j+1)

def Astar():
    pass

def manhattan():
    pass

def Sline():
    pass

def HVert():
    pass

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
        path = Astar(start, goal, heur, world)
    elif method == 'DFS':
        path = DFS(start, goal, heur, world)
    elif method == 'BFS':
        path = BFS(start, goal, heur, world)

if __name__ == "__main__":
    main()

