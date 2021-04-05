import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import pyproj
import csv
%matplotlib inline


# Set four corners of map grid
def set_corners():
    df_corners = pd.read_csv('../raw_data/fourcorners.csv', ',')
    epsg = 'epsg:3857'
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    geo_df_corners = gpd.GeoDataFrame(df_corners, crs = epsg, geometry = geometry)
    return geo_df_corners

def set_projections():
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

def get_gridpoints():
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

def coord_gridpoints(data):
    # Grid points
    df_coords_grid = pd.read_csv('testoutbsas.csv')
    gdf = gpd.GeoDataFrame(df_coords_grid, geometry=gpd.points_from_xy(df_coords_grid.lon, df_coords_grid.lat))

    # Create geodataframe with data
    gpd_data = gpd.GeoDataFrame(data,
                                crs = epsg,
                                geometry = gpd.points_from_xy(data.search_longitude, data.search_latitude))

    return gpd_data

