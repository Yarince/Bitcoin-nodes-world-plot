import gmplot

from links import LinkCreator

creator = LinkCreator()

routes = creator.create_routes()
graph = creator.graph

# for start, dist in routes.items():
# graph.printSolution(start, dist)
# creator.print_total_links()

latitude_list = [node.latitude for node in routes.keys()]
longitude_list = [node.longitude for node in routes.keys()]

gmap3 = gmplot.GoogleMapPlotter(0, 0, 1)

# scatter method of map object
# scatter points on the google map
gmap3.scatter(latitude_list, longitude_list, '# FFF000', 10, marker=True)

# Plot method Draw a line in
# between given coordinates
gmap3.plot(latitude_list, longitude_list, 'cornflowerblue', edge_width=2.5)

gmap3.draw("../map.html")
