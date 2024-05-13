#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from graph_tool.all import load_graph, shortest_path
import numpy as np
from shapely.geometry import Point
from shapely.geometry import LineString

g = load_graph("my_graph.xml.gz")

weight = g.edge_properties["weight"]
coord = g.vertex_properties["coord"]
node_dictionary = { tuple(coord[u]):u for u in g.get_vertices()}
vert_dictionary = { str(v): k for k,v in node_dictionary.items()}
graph_nodes = np.array(list(node_dictionary.keys()))

# findest N nearest nodes to point in graph
def find_n_nearest_node(point,data =  graph_nodes, n=11):
    diff = np.hypot(*(data - point).T)
    sorted_indices = np.argsort(diff)[:n]
    return  data[sorted_indices] 

# find if point lies on line
def is_on_path(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return (collinear(a, b, c)
            and (within(a[0], c[0], b[0]) if a[0] != b[0] else 
                 within(a[1], c[1], b[1])))

def collinear(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])

def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p


# project point onto line
def project_point(c, a ,b):
    point = Point(c)
    line = LineString([a, b])
    
    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n)
    return(P)

# get route from point1 to point2
def get_route(point1, point2):
    # find the 2 closest nodes to point1 and point2	
    p1s = find_n_nearest_node(point1, n=2)
    p2s= find_n_nearest_node(point2, n=2)
    
    # get the coordinates for nearest nodes
    p1 = node_dictionary[tuple(p1s[0])]
    p2 = node_dictionary[tuple(p2s[0])]

    # get shortest path    
    vertices, edges = shortest_path(g, g.vertex(p1), g.vertex(p2), weights=weight)
    
    path = [ vert_dictionary[str(vert)] for vert in vertices ]
    
    # project the original given points onto the nearest street
    point1 = project_point(point1,p1s[0],p1s[1])
    point2 = project_point(point2,p2s[0],p2s[1])
    
    # the following code is to make the starting and ending point of the polyline more accurate
    # we want to make it so the polyline will (visually) always start at point1 and end at point2	
    if is_on_path(path[0],path[1],point1):
        path_2 = [ point1, *path[1:] ]
    else:
        path_2 = [ point1, *path ]

    if is_on_path(path[-2],path[-1],point2):
        path_2 = [ *path[:-1], point2 ]
    else:
        path_2 = [ *path, point2 ]
    # we also return original path in case projection led to a point not on a street
    return path_2, path


