from geo_obj import *

class Hierarchy:
    def __init__(self) -> None:
        self.adj = dict()
        self.nodes = set()
        self.polys = list()
        self.poly_map = dict()
        self.regions = dict()
        self.triangulation = set()
        self.enclosing_triangle = Polygon((100, 0),(-100, 100),(-100, -100))
    
    def add_region(self, poly: Polygon, name: str):
        self.regions[poly] = name
        self.polys.append(poly)
    
    def add_node(self, poly: Polygon):
        self.nodes.add(poly)
        self.adj[poly] = []

    def triangulate_helper(self, polys: list[Polygon]):
        '''Bowyer-Watson Algorithm for triangulation'''
        super_t = self.enclosing_triangle
        triangulations = set([super_t])

        for poly in polys:
            vertices = poly.V
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
        for vertex in self.enclosing_triangle.V: 
            if vertex in v_set: v_set.remove(vertex)
        
        v_list = get_ccw(list(v_set))
        
        # Retriangulating
        new_triangles = self.triangulate_helper([Polygon(*v_list),])
        for tri in new_triangles: 
            self.triangulation.add(tri)
            self.add_node(tri)

        for new in new_triangles:
            for old in removed_triangles:
                if triangle_overlap(new, old):
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
