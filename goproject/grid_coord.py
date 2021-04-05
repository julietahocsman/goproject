import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_corners = pd.read_csv('../raw_data/fourcorners.csv', ',')


def set_corners():
    df_corners = pd.read_csv('../raw_data/fourcorners.csv', ',')
    epsg = 'epsg:3857'
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    geo_df_corners = gpd.GeoDataFrame(df_corners, crs = epsg, geometry = geometry)
    return geo_df_corners


def grid_coordinates(geo_df_corners, columns, rows):
    '''Generates a grid Given a dataframe (geo_df_corners) that contains the lon and lat of
    the four corners of a rectangle:
    row 0 ---> nw
    row1 ---> ne
    row 2 ---> se
    row 3 ---> sw
    of columns and rows wanted'''

    nw_lat = geo_df_corners.lat[0]
    nw_lon = geo_df_corners.lon[0]
    ne_lat = geo_df_corners.lat[1]
    ne_lon = geo_df_corners.lon[1]
    se_lat = geo_df_corners.lat[2]
    se_lon = geo_df_corners.lon[2]
    sw_lat = geo_df_corners.lat[3]
    sw_lon = geo_df_corners.lon[3]

    lat_dist = abs(nw_lat - sw_lat)
    lon_dist = abs(se_lon - sw_lon)

    list_columns = np.linspace(nw_lon,ne_lon,columns)
    list_rows = np.linspace(nw_lat,sw_lat,rows)

    grid_coordinates = {'longitude':[], 'latitude':[]}

    for row in list_rows:
        for column in list_columns:
            grid_coordinates['longitude'].append(column)
            grid_coordinates['latitude'].append(row)

    return grid_coordinates

def column_row(geo_df_corners, columns=30, rows=30, x, y):

    '''Given a dataframe (geo_df_corners) that contains the lon and lat of
    the four corners of a rectangle:
    row 0 ---> nw
    row1 ---> ne
    row 2 ---> se
    row 3 ---> sw
    And given the number of columns and rows I want in my grid, and given a
    particular location (x: lon, y:lat) it returns the column and the row that
    location belongs to'''

    nw_lat = geo_df_corners.lat[0]
    nw_lon = geo_df_corners.lon[0]
    ne_lat = geo_df_corners.lat[1]
    ne_lon = geo_df_corners.lon[1]
    se_lat = geo_df_corners.lat[2]
    se_lon = geo_df_corners.lon[2]
    sw_lat = geo_df_corners.lat[3]
    sw_lon = geo_df_corners.lon[3]

    lat_dist_total = abs(nw_lat - sw_lat)
    lon_dist_total = abs(se_lon - sw_lon)

    lat_dist_ind = lat_dist_total/rows
    lon_dist_ind = lon_dist_total/columns

    ranges_columns = []
    ranges_rows = []


    for i in range(columns+1):
        ranges_columns.append(sw_lon+(lon_dist_ind*i))
    for j in range(rows+1):
        ranges_rows.append(sw_lat+(lat_dist_ind*j))

    for i in ranges_columns:
        if abs(x) > abs(i):
            column = ranges_columns.index(i)
            break

    for i in ranges_rows:
        if abs(y) > abs(i):
            row = ranges_rows.index(i)
            break

    return column, row






















