import math as m

#for code decoration
from typing import *

line = List[List[float]]
point = List[float]
determinant = Callable



class Vertex:
    """Minimal implementation of a vertex of a 2D dcel"""

    def __init__(self, px, py):
        self.x = px
        self.y = py
        self.hedgelist = []

    def sortincident(self):
        self.hedgelist.sort(key=lambda x : x.angle)
        self.hedgelist.reverse()
        
class Hedge:
    """Minimal implementation of a half-edge of a 2D dcel"""

    def __init__(self,v1,v2):
        #The origin is defined as the vertex it points to
        self.origin = v2
        self.twin = None
        self.face = None
        self.nexthedge = None
        self.angle = hangle(v2.x-v1.x, v2.y-v1.y)
        self.prevhedge = None
        self.length = m.sqrt((v2.x-v1.x)**2 + (v2.y-v1.y)**2)

class Face:
    """Implements a face of a 2D dcel"""

    def __init__(self):
        self.wedge = None
        self.data = None
        self.external = None

    def vertexlist(self):
        h = self.wedge
        pl = [h.origin]
        while(not h.nexthedge is self.wedge):
            h = h.nexthedge
            pl.append(h.origin)
        return pl

    def isinside(self, p):
        """Determines whether a point is inside a face"""

        h = self.wedge
        inside = False
        if lefton(h, p):
            while(not h.nexthedge is self.wedge):
                h = h.nexthedge
                if not lefton(h, p):
                    return False
            return True
        else:
            return False

    def area(self):
        h = self.wedge
        a = 0
        while(not h.nexthedge is self.wedge):
            p1 = h.origin
            p2 = h.nexthedge.origin
            a += p1.x*p2.y - p2.x*p1.y
            h = h.nexthedge

        p1 = h.origin
        p2 = self.wedge.origin
        a = (a + p1.x*p2.y - p2.x*p1.y)/2
        return a


class DCEL():
    """
    Implements a doubly-connected edge list
    """

    def __init__(self, vl=[], el=[]):
        self.vertices = []
        self.hedges = []
        self.faces = []
        self.el = el
        self.vl = vl

    def build_dcel(self):
        """
        Creates the dcel from the list of vertices and edges
        """

        #Step 1: vertex list creation
        for v in self.vl:
            self.vertices.append(Vertex(v[0], v[1]))

        #Step 2: hedge list creation. Assignment of twins and 
        #vertices
        for e in self.el:
            if e[0] >= 0 and e[1] >= 0:
                h1 = Hedge(self.vertices[e[0]], self.vertices[e[1]])
                h2 = Hedge(self.vertices[e[1]], self.vertices[e[0]])
                h1.twin = h2
                h2.twin = h1
                self.vertices[e[1]].hedgelist.append(h1)
                self.vertices[e[0]].hedgelist.append(h2)
                self.hedges.append(h2)
                self.hedges.append(h1)

        #Step 3: Identification of next and prev hedges
        for v in self.vertices:
            v.sortincident()
            l = len(v.hedgelist)
            if l < 2:
                raise DcelError(
                    "Badly formed dcel: less than two hedges in vertex")
            else:
                for i in range(l-1):
                    v.hedgelist[i].nexthedge = v.hedgelist[i+1].twin
                    v.hedgelist[i+1].prevhedge = v.hedgelist[i]
                v.hedgelist[l-1].nexthedge = v.hedgelist[0].twin
                v.hedgelist[0].prevhedge = v.hedgelist[l-1]

        #Step 4: Face assignment
        provlist = self.hedges
        nf = 0
        nh = len(self.hedges)

        while nh > 0:
            h = provlist.pop()
            nh -= 1
            #We check if the hedge already points to a face
            if h.face == None:
                f = Face()
                nf += 1
                #We link the hedge to the new face
                f.wedge = h
                f.wedge.face = f
                #And we traverse the boundary of the new face
                while (not h.nexthedge is f.wedge):
                    h = h.nexthedge
                    h.face = f
                self.faces.append(f)
        #And finally we have to determine the external face
        for f in self.faces:
            f.external = f.area() < 0

    def nfaces(self):
        return len(self.faces)

    def nvertices(self):
        return len(self.vertices)

    def nedges(self):
        return len(self.hedges)/2

def hangle(dx,dy):
    """Determines the angle with respect to the x axis of a segment
    of coordinates dx and dy
    """

    l = m.sqrt(dx*dx + dy*dy)
    if dy > 0:
        return m.acos(dx/l)
    else:
        return 2*m.pi - m.acos(dx/l)

'sturucture that handles events in sweeping algorith'
class Event:
    def __init__(self, position: point, event_type: str, line: line):
        self.position = position
        self.event_type = event_type
        self.line = line
    
    #necessary comparator, the order in T structure
    def __gt__(self, other) -> bool:
        if self.position[0] == other.position[0]:
            if self.event_type == other.event_type:
                return self.position[1] < other.position[1]
            return self.event_type == 'start'
        return self.position[0] < other.position[0]


'structure that handles Line in sweeping algorithm'
class Line:
    def set_class(det: determinant, e: float =1e-8):
        Line.det = det
        Line.e = e
        
    def __init__(self, line: line):
        #standard math line parameters
        self.start = line[0]
        self.end = line[1]
        self.m = (self.start[1]-self.end[1])/(self.start[0]-self.end[0])
        self.b = (self.start[1]-self.m*self.start[0])
    
    'x axis comperator point'
    def set_ordering(x: float):
        Line.ordering_x = x
    
    def get_line(self) -> line:
        return [self.start, self.end]
    
    'necessary comparator, the order in Q structure'
    def __eq__(self, other) -> bool:
        return self.start == other.start and self.end == other.end
    
    def __gt__(self, other) -> bool:
        x = Line.ordering_x
        return self.m*x+self.b > other.m*x+other.b
    
    def __hash__(self):
        return hash(self.start) + hash(self.end)

    def __str__(self):
        return str([self.start, self.end])