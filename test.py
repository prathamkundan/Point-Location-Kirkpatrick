from algorithm import *
import json

if __name__ == "__main__":
    P1 = Polygon((20, 0),(-5, 41),(-20, 10),(-20, -20))
    P2 = Polygon((-75, 75),(-50, 25),(-75, -75))
    regions = [P2]
    region_names = ["R1","R2"]
    Algorithm(regions, region_names)