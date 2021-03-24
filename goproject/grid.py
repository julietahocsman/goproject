import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import pyproj
import csv
%matplotlib inline


# Open city map
bsas_map = gpd.read_file('../gopa_data/barrios-ciudad')

# Set four corners of map grid
df_corners = pd.read_csv('fourcorners.csv', ',')
epsg = 'epsg:3857'
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
geo_df_corners = gpd.GeoDataFrame(df_corners, crs = epsg, geometry = geometry)


# Set up projections
p_ll = pyproj.Proj('epsg:4326')
p_mt = pyproj.Proj('epsg:3857')

# Set southwest and northeast coordinates to create the grid
sw = shapely.geometry.Point((-58.538143, -34.705557))
ne = shapely.geometry.Point((-58.350345, -34.532787))
stepsize = 500 # 500 m grid step size

# Project corners to target projection
transformed_sw = pyproj.transform(p_ll, p_mt, sw.x, sw.y) # Transform NW point to 3857
transformed_ne = pyproj.transform(p_ll, p_mt, ne.x, ne.y) # .. same for SE

# Iterate over 2D area
gridpoints = []
x = transformed_sw[0]
while x < transformed_ne[0]:
    y = transformed_sw[1]
    while y < transformed_ne[1]:
        p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
        gridpoints.append(p)
        y += stepsize
    x += stepsize

# Create my grid points
with open('testoutbsas.csv', 'w') as of:
    of.write('lon,lat\n')
    for p in gridpoints:
        of.write('{:f},{:f}\n'.format(p.x, p.y))

df_coords_grid = pd.read_csv('testoutbsas.csv')
gdf = gpd.GeoDataFrame(df_coords_grid, geometry=gpd.points_from_xy(df_coords.lon, df_coords.lat))

# Bring my data
data = pd.read_json('backupPretty.json')

#Preprocess data
data = data.T
data = data.drop(columns = ['user_longitude', 'user_latitude', '__collections__'])
data.reset_index(level=0, inplace=True)
data.drop(columns="index")
data['search_method'] = data['search_method'].convert_dtypes()
data = data[data.search_method != 'startup']

# Create geodataframe with data
gpd_data = gpd.GeoDataFrame(data,
                            crs = epsg,
                            geometry = gpd.points_from_xy(data.search_longitude, data.search_latitude))

