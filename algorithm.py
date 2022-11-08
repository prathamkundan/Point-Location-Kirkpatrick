from geo_obj import *
import copy

class Hierarchy:
    def __init__(self) -> None:
        self.adj = dict()
        self.nodes = set()
        self.polys = list()
        self.poly_map = dict()
        self.regions = dict()
        self.triangulation = set()
        self.enclosing_triangle = Polygon((150, 0),(-150, 150),(-150, -150))
    
    def add_region(self, poly: Polygon, name: str):
        self.regions[poly] = name
        self.polys.append(poly)
    
    def add_node(self, poly: Polygon):
        self.nodes.add(poly) #here node is a polygon
        self.adj[poly] = []

    def retriangulate(self, poly: Polygon):
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
                        vertices.pop(index)
                        triangulations.add(T)
                        triangles_found+=1
        
        return triangulations

    def triangulate_helper(self, polys: list[Polygon]):
        '''Bowyer-Watson Algorithm for triangulation'''
        super_t = self.enclosing_triangle
        triangulations = set([super_t])

        for poly in polys:
            vertices = poly.get_ccw_vertices()
            print(f"vertices in function: {vertices}")
            for vertex in vertices:    
                bad_triangles = []
                for tpoly in triangulations:
                    if (is_inside(vertex, tpoly)):
                        bad_triangles.append(tpoly)

                p_set = []

                for bpoly in bad_triangles:
                    for edge in bpoly.E:
                        flag = True
                        for _bpoly in bad_triangles:
                            if _bpoly == bpoly: continue
                            for _edge in _bpoly.E:
                                if edge == _edge or (edge[1],edge[0]) == _edge:
                                    flag = False

                        if flag:
                            p_set.append(edge)

                for bpoly in bad_triangles:
                    triangulations.remove(bpoly)
                
                for edge in p_set:
                    [x, y, z] = get_ccw([edge[0], edge[1], vertex])
                    triangulations.add(Polygon(x, y, z))

        return triangulations

    def triangulate(self):
        
        triangulations = self.triangulate_helper(self.polys)

        for poly in self.polys:
            for tri in triangulations:
                vertices = tri.get_ccw_vertices()
                flag = True
                for vertex in vertices:
                    if vertex not in poly.V: 
                        flag = False
                        break
                if flag: self.poly_map[tri] = poly
            
        for tri in triangulations:
            self.nodes.add(tri)
            self.adj[tri] = []
        
        self.triangulation = triangulations
    
    def remove_point(self, p: Point):
        removed_triangles = set()
        for tri in self.triangulation:
            if p in tri.V: removed_triangles.add(tri)

        v_set = set()
        for tri in removed_triangles:
            for v in tri.V:
                v_set.add(v)
            self.triangulation.remove(tri)

        v_set.remove(p)
        v_list = get_ccw(list(v_set), p)
        
        print("V-list : ",v_list)

        new_triangles = self.retriangulate(Polygon(*v_list))

        # Retriangulating
        for tri in new_triangles: 
            self.triangulation.add(tri)
            self.add_node(tri)

        for new in new_triangles:
            for old in removed_triangles:
                # if triangle_overlap(new, old):
                self.adj[new].append(old)

    def select_independent_set(self):
        v_set = set()
        independent_set = set()
        off_limits = set([i for i in self.enclosing_triangle.V])

        for tri in self.triangulation:
            for vertex in tri.V: v_set.add(vertex)
        
        for vertex in v_set:
            if vertex in off_limits:
                continue
            independent_set.add(vertex)
            off_limits.add(vertex)
            for tri in self.triangulation:
                if vertex in tri.V:
                    for _vertex in tri.V: off_limits.add(_vertex)
        
        return independent_set

    def search_point(self, p: Point,triangulations):
        if not is_inside(p, self.enclosing_triangle):
            return "External Region"

        cur = None
        index = 0

        for triangle in self.triangulation:
            if PointInTriangle(p, triangle):
                cur = triangle
                plt.plot(p.x,p.y,'ro')
                #plot_poly(cur,'r-') 
                plot_polys(triangulations[index])
                index+=1
                break
    
        while self.adj[cur] != []:
            for triangle in self.adj[cur]:
                if PointInTriangle(p, triangle):
                    cur = triangle
                    plt.plot(p.x,p.y,'ro') 
                    #plot_poly(cur,'r-')
                    plot_polys(triangulations[index])
                    index+=1
                    break
        
        plt.plot(p.x,p.y,'ro') 
        #plot_poly(cur,'r-') 
        plot_polys(triangulations[index])

        if cur in self.poly_map:
            cur = self.poly_map[cur]
        return self.regions.get(cur, "External Region")


def Algorithm(regions: list[Polygon], region_names: list[str]):
    H = Hierarchy()
    tri = []

    for region, name in zip(regions, region_names):
        H.add_region(region, name)
    
    H.triangulate()
    tri.append(copy.deepcopy(H.triangulation))

    while (len(H.triangulation) > 3):
        independent_set = H.select_independent_set()

        print(independent_set)
        print(H.triangulation)

        triangulation = H.triangulation
        tri.append(copy.deepcopy(H.triangulation))
    
        plot_polys(H.triangulation)
        for polygon in H.polys:
            plot_poly(polygon, 'r-')
        for vertex in independent_set:
            print(f"removing {vertex}")
            H.remove_point(vertex)

    tri.append(copy.deepcopy(H.triangulation))

    plot_polys(H.triangulation)
    print(len(H.adj.keys()))
    tri.reverse()
    for i in tri:
        print(i)

    while (True):
        print("Enter the coordinates of the point to search: ")
        x = int(input())
        y = int(input())
        print(H.search_point(Point(x, y),tri))
        z = int(input("Enter 1 to continue the program or -1 to exit: "))
        if(z == -1):
            break
