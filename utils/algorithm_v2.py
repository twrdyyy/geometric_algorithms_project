from blist import sortedlist, sortedset
from functools import total_ordering
import math as m

def det(a, b, c):
	return a[0]*b[1] + a[1]*c[0] + b[0]*c[1] - b[1]*c[0] - a[1]*b[0] - a[0]*c[1]

def intersect(a, b):

	a = [[a.origin.x, a.origin.y], [a.twin.origin.x, a.twin.origin.y]]
	b = [[b.origin.x, b.origin.y], [b.twin.origin.x, b.twin.origin.y]]

	#start end points
	a_start, b_start, a_end, b_end = a[0], b[0], a[1], b[1]
	
	return (det(a_start, a_end, b_start) * det(a_start, a_end, b_end) < 0 and 
			det(b_start, b_end, a_start) * det(b_start, b_end, a_end) < 0)

def on(v, hedge):
	return 0 == det([v.x, v.y], [hedge.origin.x, hedge.origin.y], [hedge.twin.origin.x, hedge.twin.origin.y])

@total_ordering
class Vertex:
	def __init__(self, px, py):
		self.x = px
		self.y = py
		self.hedgelist = []

	def sortincident(self):
		self.hedgelist.sort(key=lambda x : x.angle)
		self.hedgelist.reverse()
		
	def __gt__(self, other):
		return (self.y, self.x) > (other.y, other.x)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

# @total_ordering
class Hedge:

	def __init__(self,v1,v2):
		self.origin = v2
		self.twin = None
		self.face = None
		self.nexthedge = None
		self.angle = hangle(v2.x-v1.x, v2.y-v1.y)
		self.prevhedge = None
		self.length = m.sqrt((v2.x-v1.x)**2 + (v2.y-v1.y)**2)

	# def __eq__(self, other):
	# 	return (self.origin.x, self.origin.y, self.twin.origin.x, self.twin.origin.y) == (
	# 		other.origin.x, other.origin.y, other.twin.origin.x, other.twin.origin.y)

	# def __gt__(self, other):
	# 	return (self.origin.x, self.origin.y) > (other.twin.origin.x, other.twin.origin.y)

class Face:
	def __init__(self):
		self.wedge = None
		self.data = None
		self.inner = []

	def vertexlist(self):
		h = self.wedge
		pl = [h.origin]
		while(not h.nexthedge is self.wedge):
			h = h.nexthedge
			pl.append(h.origin)
		return pl

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
		provlist = self.hedges.copy()
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

from data_structures import Line, Event

#for code decoration
from typing import *

line = List[List[float]]
point = List[float]
determinant = Callable

def r(v):
	return (round(v[0]), round(v[1])) 

def det(a: point, b: point, c: point) -> float:
	return a[0]*b[1] + a[1]*c[0] + b[0]*c[1] - b[1]*c[0] - a[1]*b[0] - a[0]*c[1]

def intersect(a: line, b: line) -> bool:
	#start end points
	a_start, b_start, a_end, b_end = a[0], b[0], a[1], b[1]
	
	return (det(a_start, a_end, b_start) * det(a_start, a_end, b_end) < 0 and 
			det(b_start, b_end, a_start) * det(b_start, b_end, a_end) < 0)

def get_Event_from_intersection(first: Line, second: Line) -> Event:
	#compute intersection point
	x = (second.b - first.b)/(first.m - second.m)
	intersection_point = (x,first.m*x+first.b)
	#create event
	return Event(intersection_point, 'cross', [first,second])

def check_intersection(first: Line, second: Line, T: sortedlist, Q: sortedset) -> None:	
	if intersect(first.get_line(), second.get_line()):
		#add intersection event to T structure
		T.add(get_Event_from_intersection(first, second))

		
def get_intersections(lines, e=1e-10, det=det):
	Line.set_class(det,e)
	T = []
	for line in lines:
		l = Line([r(line[0]), r(line[1])]) #convert line to Line structure
		T.append(Event(line[0],'start',l))
		T.append(Event(line[1],'end',l))
	T = sortedlist(T) #timeline structure declaration
	Q = sortedlist() #broom structure declaration
	Line.set_ordering(T[-1].position[0])
	intersections = set()
	while len(T) > 0:
		event = T.pop() #get most left event from x axis 
		if event.event_type == 'start':
			Line.set_ordering(event.position[0])  #set order of storing Lines in timeline structure
			Q.add(event.line) #add Line to broom structure
			b = Q.index(event.line) 
			b -= 1
			if b>=0 and b < len(Q):
				if abs(det(event.position, Q[b].get_line()[0], Q[b].get_line()[1])) < 1e-3 and (
					r(event.position) != r(Q[b].get_line()[0]) and r(event.position) != r(Q[b].get_line()[1])):
					intersections.add(r(event.position))
				   
				check_intersection(Q[b], event.line, T, Q)
			b += 2
			if b>=0 and b < len(Q):
				if abs(det(event.position, Q[b].get_line()[0], Q[b].get_line()[1])) < 1e-3 and (
					r(event.position) != r(Q[b].get_line()[0]) and r(event.position) != r(Q[b].get_line()[1])):
					intersections.add(r(event.position))
	   
				check_intersection(Q[b], event.line, T, Q)
			
		elif event.event_type == 'end':
			k = Q.index(event.line)

			b = k
			b -= 1
			if b>=0 and b < len(Q):
				if abs(det(event.position, Q[b].get_line()[0], Q[b].get_line()[1])) < 1e-3 and (
					r(event.position) != r(Q[b].get_line()[0]) and r(event.position) != r(Q[b].get_line()[1])):
					intersections.add(r(event.position))
					line = Q[b].get_line()
			b += 2
			if b>=0 and b < len(Q):
				if abs(det(event.position, Q[b].get_line()[0], Q[b].get_line()[1])) < 1e-3 and (
					r(event.position) != r(Q[b].get_line()[0]) and r(event.position) != r(Q[b].get_line()[1])): 
					intersections.add(r(event.position))

			a = k+1
			b = k-1
			if a < len(Q) and b < len(Q) and a>=0 and b>=0:	
				check_intersection(Q[a], Q[b], T, Q)
				
			Q.discard(event.line) #delete line from broom structure			
			
		else:
			if event.position in intersections:
				continue
			

			line = event.line[0].get_line()

			line = event.line[1].get_line()
			
			intersections.add(event.position) #add point to intersetion set

			Q.discard(event.line[0])
			Q.discard(event.line[1])
			
			Line.set_ordering(event.position[0])			
			Line.ordering_x += 1e-5
			Q.add(event.line[0])
			Q.add(event.line[1])

			k = Q.index(event.line[0])
			m = Q.index(event.line[1])
			
			if k > m:
				k , m = m , k
				
			if m >= 0 and m+1 < len(Q) and m+1 != k:
				check_intersection(Q[m],Q[m+1],T, Q)
			if k-1 >= 0 and k < len(Q) and k-1 != m:
				check_intersection(Q[k],Q[k-1],T, Q)
				
	return list(intersections)

def overlay(S1, S2):

	D = DCEL()
	D.vertices = S1.vertices + S2.vertices
	D.hedges = S1.hedges + S2.hedges
	D.faces = S1.faces + S1.faces
	eps = 1e-10
	vectors = [
		[eps, eps],
		[eps,-eps],
		[-eps,-eps],
		[-eps,eps]
	]
	def get_direction_of_line(beg, end):
		return (0 if end[0] - beg[0] > 0 else 2) + (1 if end[1] - beg[1] < 0 else 0)
	lines = []
	for edge in S1.el:
		v1 = S1.vl[edge[0]]
		v2 = S1.vl[edge[1]]
		if v1 > v2:
			v1, v2 = v2, v1
		vec = vectors[get_direction_of_line(v1, v2)]
		v1 = list(v1)
		v2 = list(v2)
		a = (v1[1]-v2[1])/(v1[0]-v2[0])
		b = (v1[1]-a*v1[0])
		v1[0] += vec[0]
		v1[1] = (a*v1[0] + b)
		v2[0] -= vec[0]
		v2[1] = (a*v2[0] + b)
		v1 = tuple(v1)
		v2 = tuple(v2)
		lines.append([v1, v2])
	for edge in S2.el:
		v1 = S2.vl[edge[0]]
		v2 = S2.vl[edge[1]]
		if v1 > v2:
			v1, v2 = v2, v1
		vec = vectors[get_direction_of_line(v1, v2)]
		v1 = list(v1)
		v2 = list(v2)
		a = (v1[1]-v2[1])/(v1[0]-v2[0])
		b = (v1[1]-a*v1[0])
		v1[0] += vec[0]
		v1[1] = (a*v1[0] + b)
		v2[0] -= vec[0]
		v2[1] = (a*v2[0] + b)
		v1 = tuple(v1)
		v2 = tuple(v2)
		lines.append([v1, v2])


	P = get_intersections(lines)

	print(P)

w = [(1,1), (2,2), (1,3), (0,2), (3,1), (4,2), (3,3)]
e = [[0, 1], [1, 2], [2, 3], [0, 3], [1,4], [4,5], [5,6], [6,1]]
v = [(2,1), (3,2), (2,3), (1,2), (4,1), (5,2), (4,3)]

w = [(1,1), (2,2), (1,3), (0,2)]
v = [(3, 1), (4, 2), (3, 3), (2, 2)]
e = [[0, 1], [1, 2], [2, 3], [0, 3]]

S1 = DCEL(w, e)
S2 = DCEL(v, e)

S1.build_dcel()
S2.build_dcel()

overlay(S1, S2)
