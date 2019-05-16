import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

from links import LinkCreator
from nodes_fetcher import NodeHandler, Node

np.random.seed(42)

creator = LinkCreator()

graph = creator.create_links()
creator.print_total_links()
parser = NodeHandler()

# create new figure, axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# setup mercator map projection.

# set perspective angle
lat_viewing_angle = 50
lon_viewing_angle = -73

# define color maps for water and land
ocean_map = (plt.get_cmap('ocean'))(210)
cmap = plt.get_cmap('gist_earth')

# call the basemap and use orthographic projection at viewing angle
m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')

start: Node
for start, nodes in graph.graph.items():
    end: Node
    for end in nodes:
        m.drawgreatcircle(start.longitude, start.latitude, end.longitude, end.latitude, linewidth=2, color='b')

m.drawcoastlines()
m.fillcontinents()
# draw parallels
m.drawparallels(np.arange(10, 90, 20), labels=[1, 1, 0, 1])
# draw meridians
m.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1])
ax.set_title('Bitcoin nodes and miners')
plt.show()
