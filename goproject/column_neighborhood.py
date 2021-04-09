import pandas as pd
import geopandas as gpd
from goproject.get_data import preproc
import warnings
warnings.filterwarnings('ignore')

def merging_neighbor_dataframes():

    neighborhood_list = ['chacarita',
    "paternal",
    'villa crespo',
    'villa del parque',
    'almagro',
    'caballito',
    'dique 3',
    'villa santa rita',
    'monte castro',
    'villa real',
    'flores',
    'floresta',
    'constitucion',
    'belgrano',
    'recoleta',
    'retiro',
    'san cristobal',
    'boedo',
    'velez sarsfield',
    'villa luro',
    'parque patricios',
    'mataderos',
    'villa lugano',
    'escollera exterior',
    'nuñez',
    'boca',
    'dique 2',
    'san telmo',
    'saavedra',
    'coghlan',
    'villa urquiza',
    'colegiales',
    'balvanera',
    'dique 4',
    'villa gral. mitre',
    'dique 1',
    'parque chas',
    'agronomia',
    'villa ortuzar',
    'barracas',
    'parque avellaneda',
    'parque chacabuco',
    'nueva pompeya',
    'palermo',
    'villa riachuelo',
    'villa soldati',
    'villa pueyrredon',
    'villa devoto',
    'liniers',
    'versalles',
    'puerto madero',
    'monserrat',
    'san nicolas'
        ]

    list_upper = []

    for i in neighborhood_list:
        neighbor = i.upper()
        list_upper.append(neighbor)

    gpd_dataframes_list = []

    bsas_map = gpd.read_file('../gopa_data/barrios-ciudad')
    bsas_map['BARRIO'][6] = 'DIQUE 3'
    bsas_map['BARRIO'][24] = 'NUÑEZ'
    bsas_map['BARRIO'][26] = 'DIQUE 2'
    bsas_map['BARRIO'][33] = 'DIQUE 4'
    bsas_map['BARRIO'][35] = 'DIQUE 1'

    coordinates = preproc('../raw_data/dataBackup.json')


    for neighbor in list_upper:
        gpd_data = gpd.GeoDataFrame(coordinates,
                         geometry = gpd.points_from_xy(coordinates.search_longitude, coordinates.search_latitude))

        polygon_neighbor = bsas_map[bsas_map['BARRIO'] == neighbor].geometry
        gpd_data ['neighbor'] = gpd_data.apply(lambda x: polygon_neighbor.contains(x.geometry), axis=1)
        gpd_data ['neighbor'] = gpd_data ['neighbor'].apply(lambda x: 0 if x == False else neighbor)
        gpd_data = gpd_data[gpd_data.neighbor != 0]
        gpd_dataframes_list.append(gpd_data)

    all_data = pd.concat(gpd_dataframes_list)

    return all_data

