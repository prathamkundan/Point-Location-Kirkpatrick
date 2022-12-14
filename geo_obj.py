from math import atan2, degrees
import matplotlib.pyplot as plt

class Point:
    '''
    Point
    --------
    Takes x-coordinate and y-coordinate and returns a point object
    '''
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return (self.x == __o.x and self.y==__o.y)
  
    def __add__(self, __o):
        return Point((self.x+__o.x), (self.y+__o.y))

    def __sub__(self, __o):
        return Point((self.x-__o.x), (self.y-__o.y))
    
    def __truediv__(self, __o: int):
        return Point(self.x/__o, self.y/__o)
    
    def __hash__(self) -> int:
        return hash(self.__repr__())

class Polygon:
    '''
    Polygon
    --------
    Takes a set of vertices in counter clockwise order and returns a polygon object
    '''
    def __init__(self, *vertices): 
        if (len(vertices) < 3): raise ValueError("Polygon of less than 3 sides is not possible")
            
        self.V = []
        temp = []
        for pt in vertices:
            if isinstance(pt, Point):
                self.V.append(pt)
                temp.append(pt)
            else:
                self.V.append(Point(pt[0], pt[1]))
                temp.append(Point(pt[0], pt[1]))
        
        self.n = len(self.V)

        self.E = []
        for i in range(self.n):
            self.E.append((temp[i], temp[(i+1)%self.n]))
    
    def get_ccw_vertices(self):
        return self.V

    def __repr__(self) -> str:
        return f"Polygon({self.V})"

    def __str__(self) -> str:
        return f"{self.V}"
    
    def __eq__(self, __o: object) -> bool:
        return self.V == __o.V

    def __hash__(self):
        return hash(self.__repr__())
    
def is_inside(A: Point, P: Polygon) -> bool:
    '''Checks is point A is inside the circumcircle of triangle P'''

    if P.n > 3: raise(ValueError("Funtion only works for triangles"))


    [a,b,c] =[e[0] for e in P.E]
    ax_ = a.x-A.x
    ay_ = a.y-A.y
    bx_ = b.x-A.x
    by_ = b.y-A.y
    cx_ = c.x-A.x
    cy_ = c.y-A.y
    return ((
        (ax_*ax_ + ay_*ay_) * (bx_*cy_-cx_*by_) -
        (bx_*bx_ + by_*by_) * (ax_*cy_-cx_*ay_) +
        (cx_*cx_ + cy_*cy_) * (ax_*by_-bx_*ay_)
    ) > 0)
         

def get_ccw(pts: list[Point], interior = None)->list[Point]:
    '''Sorts list of points in counter-clockwise order'''

    cent = sum(pts, Point(0,0))/len(pts)
    if (interior is not None):
        cent = interior
    
    if interior is not None:
        cent = interior
    
    pts.sort(key = lambda a: (degrees(atan2(a.x - cent.x, a.y - cent.y)) + 360 % 360), reverse=True)
    return pts          

def plot_poly(P: Polygon, ocol = "k-", show = True):
    '''Plots a polygon'''
    for (p1,p2) in P.E:
        plt.plot([p1.x, p2.x], [p1.y, p2.y], ocol)
    if (show): plt.show()

def plot_polys(T: set[Polygon], show = True):
    '''Plots a set of polygons'''
    for poly in T:
        plot_poly(poly, show = False)
    if (show): plt.show()

def point_in_triangle (pt: Point, poly: Polygon)->bool:
    '''Checks if point is in triangle'''
    def sign (p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);

    if (poly.n > 3): raise ValueError("Function only works on triangles")

    [v1, v2, v3] = poly.V

    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not(has_neg and has_pos)