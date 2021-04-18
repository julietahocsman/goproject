import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')



def get_data(data_path):
    '''returns a DataFrame with search tracks'''
    data = pd.read_json(data_path)
    data = pd.DataFrame.from_dict(data['__collections__']["search_track"])
    return data


def preprocess_data(data):
    data = data.T
    data = data.drop(columns = ['user_longitude', 'user_latitude', '__collections__'])
    data.reset_index(level=0, inplace=True)
    data.drop(columns="index")
    data['search_method'] = data['search_method'].convert_dtypes()
    
   
    data.drop(columns='index', inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'], utc=True, errors='coerce')
    data['arrive'] = pd.to_datetime(data['arrive'], utc=True, errors='coerce')
    data['leave'] = pd.to_datetime(data['leave'], utc=True, errors='coerce')
    data['timestamp'] = data.timestamp.dt.strftime("%Y-%m-%d %H:%M:%S")
    data['arrive'] = data.arrive.dt.strftime("%Y-%m-%d %H:%M:%S")
    data['leave'] = data.leave.dt.strftime("%Y-%m-%d %H:%M:%S")
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['arrive'] = pd.to_datetime(data['arrive'])
    data['leave'] = pd.to_datetime(data['leave'])
    data = data[data['uid'] != 'W2UoC9eld8MNS08rn8W2KVqKCYB2']
    data = data[data['uid'] != 'REwY2MGhNFSmVq4smD6dgXBniu83']
    data = data[data['uid'] != 'RMnlCQYA06TyfsrGhw8Rscp6dTp1']
    data = data[data['uid'] != 'BLLbW2aUT4Xd5Kyu4lUX98MMget1']
    data = data[data['search_method'] != 'startup']

    ciudad['hour'] = ciudad['arrive'].dt.hour
    ciudad['month_number'] = ciudad.arrive.dt.month
    ciudad['month_name'] = ciudad.arrive.dt.month_name()
    ciudad['weekday'] = ciudad.arrive.dt.weekday
    ciudad['weekday_name'] = ciudad.arrive.dt.day_name()
    return data

def preproc(data_path):
    data = get_data(data_path)
    return preprocess_data(data)

def search_neighborhood(neighborhood, coordinates):

    bsas_map = gpd.read_file('../../gopa_data/barrios-ciudad')
    neighborhood = neighborhood.upper()
    gpd_data = gpd.GeoDataFrame(coordinates,
                         geometry = gpd.points_from_xy(coordinates.search_longitude, coordinates.search_latitude))
    reservas_bsas = gpd_data[['geometry']]
    reservas_bsas = reservas_bsas.set_crs("EPSG:4326")

    if neighborhood == 'CIUDAD':
        df_barrio = bsas_map
        fig,ax = plt.subplots(figsize = (15,16))
        bsas_map.plot(ax=ax, color='lightgrey')
        gpd_data.plot(ax=ax, markersize=5, color='red')
        ax.set_xlim([-58.550, -58.325])
        ax.set_ylim([-34.700, -34.525])
        plt.show()

    else:

        try:
            df_barrio = bsas_map[bsas_map['BARRIO'] == neighborhood]
            reservas_barrio = reservas_bsas.within(df_barrio)
            cond_reservas_barrio = gpd_data.apply(lambda x: df_barrio.contains(x.geometry), axis=1)
            gpd_data['reservas_barrio'] = cond_reservas_barrio
            gpd_data = gpd_data[gpd_data.reservas_barrio == True]
            #fig,ax = plt.subplots(figsize = (15,16))
            #bsas_map.plot(ax=ax, color='lightgrey')
            #gpd_data.plot(ax=ax, markersize=5, color='red')
            #ax.set_xlim([-58.550, -58.325])
            #ax.set_ylim([-34.700, -34.525])
            #plt.show()
        except ValueError:
            print(f"Please enter another neighborhood, {neighborhood} not found")


    return gpd_data



def filtrador(barrios ):
    data = preproc('../../raw_data/dataBackup.json')

    #cargo el dataset entero
    gpd_data = gpd.GeoDataFrame(data,
                         geometry = gpd.points_from_xy(data.search_longitude, data.search_latitude))
    
    
    bsas_map = gpd.read_file('../../gopa_data/barrios-ciudad')

    bsas_map.BARRIO = bsas_map.BARRIO.map(lambda x: x.upper()) #hago upper todo
    #elimino lo necesario y seteo el barrio como índice para fácil acceso
    bsas_map =bsas_map.set_index('BARRIO').drop(columns = ['COMUNA','GEOJSON']) 
    bsas_map = bsas_map.T  #transpongo para fácil acceso con bsas_map['BARRIO'][0]
    
    #paso todo a upper por si las dudas
    barrios = [barrio.upper() for barrio in barrios]
    
    if barrios[0] not in bsas_map.T:
        print(f'{barrios[0]} no se encuentra o no se reconoce. Quizas un error de tipeo?')
        return None
    
    filtro = gpd_data.within(bsas_map[barrios[0]] [0])
    resultados = gpd_data[filtro]
    resultados['BARRIO'] = barrios[0]
    no_encontrados =[]

    if len(barrios) > 1:
        for barrio in barrios[1:]: #comienzo a filtrar el DF
            if barrio in bsas_map.columns:
                filtro = gpd_data.within(bsas_map[barrio][0])
                nuevo_barrio = gpd_data[filtro]
                nuevo_barrio['BARRIO'] = barrio
                resultados = pd.concat([resultados, nuevo_barrio], ignore_index = True)
            else :
                print(f'{barrio} no se encuentra o no se reconoce')
                no_encontrados.append(barrio)
                
    if len(no_encontrados) != 0:
        print(no_encontrados , 'no han sido procesados')
    
    return resultados



def exportar(df):
    df.to_csv('ciudad_barrios.csv')