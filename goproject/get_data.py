import pandas as pd
import geopandas as gpd
import csv


def get_data():
    '''returns a DataFrame with search tracks'''
    data = pd.read_json('backupPretty.json')
    return data

def preprocess_data(data):
    data = data.T
    data = data.drop(columns = ['user_longitude', 'user_latitude', '__collections__'])
    data.reset_index(level=0, inplace=True)
    data.drop(columns="index")
    data['search_method'] = data['search_method'].convert_dtypes()
    data = data[data.search_method != 'startup']
    return data

if __name__ == '__main__':
    df = get_data()



