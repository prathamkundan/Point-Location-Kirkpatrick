from geo_obj import *

def retriangulate(poly: Polygon):
    triangulations = set()
    vertices = [v for v in poly.V]
    triangles_found = -1
    while (triangles_found != 0):
        triangles_found = 0
        for index, vertex in enumerate(vertices):
            next = vertices[(index+1)%len(vertices)]
            prev = vertices[index-1]

            v1 = next-vertex
            v2 = prev-vertex

            if (v1.x*v2.y - v1.y*v2.x > 0):
                ccw_vertices = get_ccw([vertex, prev, next])
                T = Polygon(*ccw_vertices)
                inside = [is_inside(v, T) for v in poly.V]
                if True in inside:
                    continue
                else:
                    print(vertices[index]) 
                    triangles_found+=1
                    vertices.pop(index)
                    triangulations.add(T)
    
    return triangulations

P1 = Polygon((-75, -75), (-50, 25), (-20, 10), (20, 0), (100, 0), (-100, 100), (-100, -100))
s = retriangulate(P1)

plot_poly(P1, "-r")
# plt.show()
plot_polys(s)