#data structures used in algorithm
from blist import sortedset, sortedlist
from utils.data_structures import Line, Event

#for code decoration
from typing import *

line = List[List[float]]
point = List[float]
determinant = Callable

'determinant function' 
def det(a: point, b: point, c: point) -> int:
    return a[0]*b[1] + a[1]*c[0] + b[0]*c[1] - b[1]*c[0] - a[1]*b[0] - a[0]*c[1]

'a bit tricky intersection checker'
def intersect(a: line, b: line) -> bool:
    #start end points
    a_start, b_start, a_end, b_end = a[0], b[0], a[1], b[1]
    
    return (det(a_start, a_end, b_start) * det(a_start, a_end, b_end) < 0 and 
            det(b_start, b_end, a_start) * det(b_start, b_end, a_end) < 0)

'create event from intersection of two lines'
def get_Event_from_intersection(first: Line, second: Line) -> Event:
    #compute intersection point
    x = (second.b - first.b)/(first.m - second.m)
    intersection_point = (x,first.m*x+first.b)
    #create event
    return Event(intersection_point, 'cross', [first,second])

'check if two lines intersect'
def check_intersection(first: Line, second: Line, T: sortedlist, Q: sortedset) -> None:    
    if intersect(first.get_line(), second.get_line()):
        #add intersection event to T structure
        T.add(get_Event_from_intersection(first, second))

        
'sweeping algorithm to detect intersection points'
def get_intersections(lines: List[line], e: float =1e-14, det: determinant =det) -> List[point]:
    
    #dict of lines for O(1) eddting at intersection point
    L = dict()
    
    #set line determinant and epsilon for error
    Line.set_class(det,e)
    
    #fill T structure with start and end point events
    T = []
    for line in lines:
        l = Line(line) #convert line to Line structure
        T.append(Event(line[0],'start',l))
        T.append(Event(line[1],'end',l))
        L[l] = 1
    
    T = sortedlist(T) #timeline structure declaration
    Q = sortedset() #broom structure declaration
    
    #order of storing Lines in timeline structure
    Line.set_ordering(T[-1].position[0])
    
    #intersection points set
    intersections = set()
    
    while len(T) > 0:
        
        event = T.pop() #get most left event from x axis 
        
        #start of the Line case
        if event.event_type == 'start':
            
            Line.set_ordering(event.position[0])  #set order of storing Lines in timeline structure
            Q.add(event.line) #add Line to broom structure
            
            #check new possible intersections for line below and above newly added line
            b = Q.index(event.line) 
            b -= 1
            if b>=0 and b < len(Q):                
                check_intersection(Q[b], event.line, T, Q)
            
            b += 2
            if b>=0 and b < len(Q):
                check_intersection(Q[b], event.line, T, Q)
            
            
        #end of Line case
        elif event.event_type == 'end':
            
            #check new possible intersections for line below and above lately deleted line
            k = Q.index(event.line)
            a = k+1
            b = k-1
            if a < len(Q) and b < len(Q) and a>=0 and b>=0:    
                check_intersection(Q[a], Q[b], T, Q)
                
            Q.discard(event.line) #delete line from broom structure            
            
        #intersection of two Lines case     
        else:
            #do not handle event that already occured 
            if event.position in intersections:
                continue
            
            #delete lines from structure
            L[event.line[0]] = 0
            L[event.line[1]] = 0
            #add four new lines to structure
            L[Line([event.line[0].get_line()[0], event.position])] = 1
            L[Line([event.position, event.line[0].get_line()[1]])] = 1
            L[Line([event.line[1].get_line()[0], event.position])] = 1
            L[Line([event.position, event.line[1].get_line()[1]])] = 1
            
            
            intersections.add(event.position) #add point to intersetion set
            
            #change Line ordering in broom set: s, s' = s', s 
            Q.discard(event.line[0])
            Q.discard(event.line[1])
            
            Line.set_ordering(event.position[0])            
            Line.ordering_x += 1e-5
            Q.add(event.line[0])
            Q.add(event.line[1])
              
            #check new possible intersections
            k = Q.index(event.line[0])
            m = Q.index(event.line[1])
            
            if k > m:
                k , m = m , k
                
            if m >= 0 and m+1 < len(Q) and m+1 != k:
                check_intersection(Q[m],Q[m+1],T, Q)
            if k-1 >= 0 and k < len(Q) and k-1 != m:
                check_intersection(Q[k],Q[k-1],T, Q)
                
    return list(intersections), L #convert set() to list()