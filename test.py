from algorithm import *

def Algorithm(regions: list[Polygon], region_names: list[str]):
    H = Hierarchy()

    for region, name in zip(regions, region_names):
        H.add_region(region, name)
    
    H.triangulate()

    while (len(H.triangulation) > 3):
        independent_set = H.select_independent_set()

        print(independent_set)
        print(H.triangulation)


        plot_polys(H.triangulation)
        for vertex in independent_set:
            print(f"removing {vertex}")
            H.remove_point(vertex)

    plot_polys(H.triangulation)
    print(H.adj)

if __name__ == "__main__":
    P1 = Polygon((20, 0),(-20, 10),(-20, -20))
    P2 = Polygon((-25, -75),(-20, -75),(-22, 10))

    plot_poly(P1, 'g-')
    plot_poly(P2, 'r-')

    regions = [P1,P2]
    region_names = ["R1",""]

    Algorithm(regions, region_names)