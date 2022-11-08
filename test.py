from algorithm import *
import json

def Algorithm(regions: list[Polygon], region_names: list[str]):
    H = Hierarchy()

    for region, name in zip(regions, region_names):
        H.add_region(region, name)
    
    H.triangulate()

    while (len(H.triangulation) > 3):
        independent_set = H.select_independent_set()

        print(independent_set)
        # print(H.triangulation)

        plot_polys(H.triangulation)
        for polygon in H.polys:
            plot_poly(polygon, 'r-')
        for vertex in independent_set:
            print(f"removing {vertex}")
            H.remove_point(vertex)

    plot_polys(H.triangulation)
    print(len(H.adj.keys()))

    while (True):
        x = int(input())
        y = int(input())
        print(H.search_point(Point(x, y)))

if __name__ == "__main__":
    P1 = Polygon((20, 0),(-5, 41),(-20, 10),(-20, -20))
    P2 = Polygon((-75, 75),(-50, 25),(-75, -75))


    regions = [P2,P1]
    region_names = ["R2","R1"]
    Algorithm(regions, region_names)