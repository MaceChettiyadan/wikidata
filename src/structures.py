#https://emekadavid-solvingit.blogspot.com/2020/08/classes-for-graphs-and-directed-graphs.html

class Node(object):
  def __init__(self, name):
    # initialise a node object with a name
    self._name = name
  
  def get_name(self):
    #get name
    return self._name

  def __str__(self):
    #str method
    return self._name

class Edge(object):
  def __init__(self, src, dest):
    #initialise an edge between two nodes
    self._src = src
    self._dest = dest

  def get_src(self):
    #get source node
    return self._src

  def get_dest(self):
    #get destination node
    return self._dest

  def __str__(self):
    #str method
    return self._src.get_name() + " -> " + self._dest.get_name()

class DirectedGraph(object):
  def __init__(self):
    #a full directed graph of nodes and edges
    self._nodes = []
    self._edges = {}

  def add_node(self, node):
    #add a node to the graph
    if node in self._nodes:
        return False
    else:
        self._nodes.append(node)
        self._edges[node] = []

  def add_edge(self, edge):
    #add an edge to the graph
    src = edge.get_src()
    dest = edge.get_dest()
    if not (src in self._nodes and dest in self._nodes):
        raise ValueError('Node not in graph')
    self._edges[src].append(dest)

  def children_of(self, node):
    #return the children of a node
    return self._edges[node]

  def has_node(self, node):
    #return a boolean of whether a node is in the graph
    return node in self._nodes

  def __str__(self):
    print(self._nodes)
    print(self._edges)
    #str method
    result = ''
    for src in self._nodes:
        for dest in self._edges[src]:
            result = result + src.get_name() + \
                '--->' + dest.get_name() + '\n'
    return result[:-1]
  


