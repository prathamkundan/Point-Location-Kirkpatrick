from algorithm import *
import json

if __name__ == "__main__":
    # P = Point(-75,75)
    # P_ = Polygon((-50,25),(-150,150),(-150,-150))
    # print(is_inside(P, P_))
    # P1 = Polygon((20, 0),(-5, 41),(-20, 10),(-20, -20))
    P2 = Polygon((-75, 75),(-50, 25),(-75, -75))
    regions = [P2]
    region_names = ["R2"]
    Algorithm(regions, region_names)