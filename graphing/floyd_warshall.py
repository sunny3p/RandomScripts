class Graph:
    def __init__(self):
        self.vertices = {}
 
    def add_vertex(self, key):
        vertex = Vertex(key)
        self.vertices[key] = vertex
 
    def get_vertex(self, key):
        return self.vertices[key]
 
    def __contains__(self, key):
        return key in self.vertices
 
    def add_edge(self, src_key, dest_key, weight=1):
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)
 
    def does_edge_exist(self, src_key, dest_key):
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])
 
    def __len__(self):
        return len(self.vertices)
 
    def __iter__(self):
        return iter(self.vertices.values())
 
 
class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}
 
    def get_key(self):
        return self.key
 
    def add_neighbour(self, dest, weight):
        self.points_to[dest] = weight
 
    def get_neighbours(self):
        return self.points_to.keys()
 
    def get_weight(self, dest):
        return self.points_to[dest]
 
    def does_it_point_to(self, dest):
        return dest in self.points_to
 
 
def floyd_warshall(g):
    distance = {v:dict.fromkeys(g, float('inf')) for v in g}
    next_v = {v:dict.fromkeys(g, None) for v in g}
 
    for v in g:
        for n in v.get_neighbours():
            distance[v][n] = v.get_weight(n)
            next_v[v][n] = n
 
    for v in g:
         distance[v][v] = 0
         next_v[v][v] = None
 
    for p in g: 
        for v in g:
            for w in g:
                if distance[v][w] > distance[v][p] + distance[p][w]:
                    distance[v][w] = distance[v][p] + distance[p][w]
                    next_v[v][w] = next_v[v][p]
 
    return distance, next_v
 
 
def print_path(next_v, u, v):
    
    p = u
    while (next_v[p][v]):
        print('{} -> '.format(p.get_key()), end='')
        p = next_v[p][v]
    print('{} '.format(v.get_key()), end='')
 
 
g = Graph()
print('Menu')
print('add vertex <key>')
print('add edge <src> <dest> <weight>')
print('floyd-warshall')
print('display')
print('quit')
 
while True:
    do = input('What would you like to do? ').split()
 
    operation = do[0]
    if operation == 'add':
        suboperation = do[1]
        if suboperation == 'vertex':
            key = int(do[2])
            if key not in g:
                g.add_vertex(key)
            else:
                print('Vertex already exists.')
        elif suboperation == 'edge':
            src = int(do[2])
            dest = int(do[3])
            weight = int(do[4])
            if src not in g:
                print('Vertex {} does not exist.'.format(src))
            elif dest not in g:
                print('Vertex {} does not exist.'.format(dest))
            else:
                if not g.does_edge_exist(src, dest):
                    g.add_edge(src, dest, weight)
                else:
                    print('Edge already exists.')
 
    elif operation == 'floyd-warshall':
        distance, next_v = floyd_warshall(g)
        print('Shortest distances:')
        for start in g:
            for end in g:
                if next_v[start][end]:
                    print('From {} to {}: '.format(start.get_key(),
                                                    end.get_key()),
                            end = '')
                    print_path(next_v, start, end)
                    print('(distance {})'.format(distance[start][end]))
 
    elif operation == 'display':
        print('Vertices: ', end='')
        for v in g:
            print(v.get_key(), end=' ')
        print()
 
        print('Edges: ')
        for v in g:
            for dest in v.get_neighbours():
                w = v.get_weight(dest)
                print('(src={}, dest={}, weight={}) '.format(v.get_key(),
                                                             dest.get_key(), w))
        print()
 
    elif operation == 'quit':
        break
