
def build(lines):
    world = []
    lineno = 0
    for line in lines:
        vals = line.split(' ')
        for i, val in enumerate(vals):
            if val == 's':
                start = [lineno, i]
            if val == 'g':
                goal = [lineno, i]
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
    search = 'A*'       # Default to A* search
    heur = 'SLine'      # Default to Straight-line heuristic

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-i':
            path = os.path.abspath(sys.argv[i+1])
        if sys.argv[i] == '-a':
            search = sys.argv[i+1]
        if sys.argv[i] == '-h':
            heur = sys.argv[i+1]
    if path == '':
        exit(1)

    fp = open(path, 'r', encoding='utf-8')
    lines = fp.readlines()
    fp.close()
    width = lines[0]
    height = lines[1]
    del lines[0]
    del lines[1]
    start, goal, world = build(lines)


if __name__ == "__main__":
    main()

