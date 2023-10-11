def build():
    world = []
    

def BFS():
    pass

def DFS():
    pass

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
    
    world = build(lines)
    
    

if __name__ == "__main__":
    main()

