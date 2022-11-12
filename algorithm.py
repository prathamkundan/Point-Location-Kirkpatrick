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
        '''Retriangulates polygon'''
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
                    inside = [point_in_triangle(v, T) for v in vertices]
                    if inside.count(True) > 3:
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

                edges = []
                for tri in bad_triangles:
                    for edge in tri.E:
                        temp_e = edge
                        if (temp_e[0].x == temp_e[1].x):
                            if (temp_e[1].y < temp_e[0].y): temp_e = (temp_e[1], temp_e[0])
                        elif (temp_e[1].x < temp_e[0].x):
                            temp_e = (temp_e[1], temp_e[0])
                        edges.append(temp_e)
                
                p_set = filter(lambda x: edges.count(x) == 1, edges)
            
                for bpoly in bad_triangles:
                    triangulations.remove(bpoly)
                
                for edge in p_set:
                    [x, y, z] = get_ccw([edge[0], edge[1], vertex])
                    triangulations.add(Polygon(x, y, z))

        return triangulations

    def triangulate(self):
        '''Triangulates polygon'''
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
                # mapping the triangulations with polygons if there is any overlapping
        for tri in triangulations:
            self.nodes.add(tri)
            self.adj[tri] = []
        
        self.triangulation = triangulations
    
    def remove_point(self, p: Point):
        '''Function to remove point from a triangulation and retriangulate the hole'''
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
        '''Function to select an independent set from a set of points'''
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
        '''Function to search point in hierarchy'''
        if not point_in_triangle(p, self.enclosing_triangle):
            return "External Region"

        cur = None
        index = 0

        for triangle in self.triangulation:
            if point_in_triangle(p, triangle):
                cur = triangle

                '''----- For plotting purposes -----'''
                plt.plot(p.x,p.y,'ro')
                # plot_polys(triangulations[index], show= False)
                plot_poly(self.enclosing_triangle,'b-', show=False) 
                plot_poly(triangle,'r-') 
                index+=1
                '''---------------------------------'''

                break
    
        while self.adj[cur] != []:
            for triangle in self.adj[cur]:
                if point_in_triangle(p, triangle):
                    '''----- For plotting purposes -----'''
                    plt.plot(p.x,p.y,'ro') 
                    # plot_polys(triangulations[index], show = False)
                    plot_poly(self.enclosing_triangle,'b-', show=False) 
                    plot_poly(triangle,'r-', show=True) 
                    index+=1
                    '''---------------------------------'''
                    cur = triangle
                    
                    break
        
        plt.plot(p.x,p.y,'ro') 
        plot_polys(triangulations[-1], show = False)

        if cur in self.poly_map:
            cur = self.poly_map[cur]
            plot_poly(cur, 'g-', show = False)
        plt.show()
        return self.regions.get(cur, "External Region")


def Algorithm(regions: list[Polygon], region_names: list[str]):
    ''' 
    Kirkpartick's Point Location Algorithm
    -----
    Preprocesses the input and runs search 
    '''
    H = Hierarchy()
    tri = []

    for region, name in zip(regions, region_names):
        H.add_region(region, name)
    
    H.triangulate()
    tri.append(copy.deepcopy(H.triangulation))

    while (len(H.triangulation) > 3):

        '''----- For plotting puposes -----'''
        tri.append(copy.deepcopy(H.triangulation))
        plot_polys(H.triangulation, show=False)
        for polygon in H.polys: plot_poly(polygon, 'r-', show=False)
        plt.show()
        '''--------------------------------'''

        independent_set = H.select_independent_set()

        for vertex in independent_set:
            print(f"Removing {vertex}")
            H.remove_point(vertex)

     
    '''----- For plotting puposes -----'''
    tri.append(copy.deepcopy(H.triangulation))
    tri.reverse()
    plot_polys(H.triangulation, show=False)
    for polygon in H.polys: plot_poly(polygon, 'r-', show=False)
    plt.show()
    '''--------------------------------'''


    while (True):
        print("Enter the coordinates of the point to search: ")
        [x, y] = map(float,input().split())
        print("Point is in: ", H.search_point(Point(x, y),tri))
        z = input("Enter 1 to continue the program or -1 to exit: ")
        if(z == '-1'):
            break
