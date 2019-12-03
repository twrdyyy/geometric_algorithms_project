def overlay_of_subdivision(S1, S2):
        
    #Firstly let's get list of lines from Dcel.el and Dcel.vl lists
    lines = []
    S1_lines = []
    for edge in S1.el:
        v1 = S1.vl[edge[0]]
        v2 = S1.vl[edge[1]]

        if v1 > v2:
            v1, v2 = v2, v1

        vec = vectors[get_direction_of_line(v1, v2)]

        v1 = list(v1)
        v2 = list(v2)

        v1[0] += vec[0]
        v1[1] += vec[1]
        v2[0] -= vec[0]
        v2[1] -= vec[1]

        v1 = tuple(v1)
        v2 = tuple(v2)

        S1_lines.append([v1, v2])
        lines.append([v1, v2])

    S2_lines = []  
    for edge in S2.el:
        v1 = S2.vl[edge[0]]
        v2 = S2.vl[edge[1]]

        if v1 > v2:
            v1, v2 = v2, v1

        vec = vectors[get_direction_of_line(v1, v2)]

        v1 = list(v1)
        v2 = list(v2)

        v1[0] += vec[0]
        v1[1] += vec[1]
        v2[0] -= vec[0]
        v2[1] -= vec[1]

        v1 = tuple(v1)
        v2 = tuple(v2)



        S2_lines.append([v1, v2])
        lines.append([v1, v2])
    
    
    
    #compute intersection points of lines list
    P, L = get_intersections(lines)
    #P = list of intersetion points
    #L = list of new lines for D structure    
    
    D_vl = S1.vl + S2.vl + P 
    
    #delete possible repetition
    D_vl = list(set(D_vl))
    
    #tmp dict for O(1) access to index of vertex
    vertices = { p : idx for idx, p in enumerate(D_vl) }
        
    #mental disease 
    D_el = [[vertices[x], vertices[y]] for x, y in [x.get_line() for x in L if L[x] == 1]]
    
    #now create DCEL structure for D
    D = DCEL(D_vl, D_el)
    
    #and build all vertices, half-edges and faces
    D.build_dcel()
    
    return D