import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap
from nodes_fetcher import Node, NodeHandler

np.random.seed(42)

parser = NodeHandler()

honest_miners, dishonest_miners, relays = parser.get_selected_nodes()




df = pd.DataFrame({"lon1": np.random.randint(-15, 30, 10),
                   "lat1": np.random.randint(33, 66, 10),
                   "lon2": np.random.randint(-15, 30, 10),
                   "lat2": np.random.randint(33, 66, 10)})

m = Basemap(llcrnrlon=-12, llcrnrlat=30, urcrnrlon=50, urcrnrlat=69.,
            resolution='i', projection='tmerc', lat_0=48.9, lon_0=15.3)

m.drawcoastlines(linewidth=0.72, color='gray')
m.drawcountries(zorder=0, color='gray')

lon1, lat1 = m(df.lon1.values, df.lat1.values)
lon2, lat2 = m(df.lon2.values, df.lat2.values)

pts = np.c_[lon1, lat1, lon2, lat2].reshape(len(lon1), 2, 2)
plt.gca().add_collection(LineCollection(pts, color="crimson", label="Lines"))

m.plot(lon1, lat1, marker="o", ls="", label="Start")
m.plot(lon2, lat2, marker="o", ls="", label="Fin")

plt.legend()
plt.show()
