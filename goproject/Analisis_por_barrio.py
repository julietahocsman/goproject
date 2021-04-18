import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import warnings
#import goproject.data
#warnings.filterwarnings('ignore')

#######################################
#####################################

#plot_barrios --  ploteamos en un mapa de buenos aires

############

#distribucion_por_dia -- genero una serie con las distribuciones de frecuencias por día

#agregador -- agrego lo que devuelve la función anterior en franjas horarias

#plotear_dia -- ploteo el día en cuestion, resultante de la funcion agregador

##############

#frecuencias_df  -- devuelvo un dataframe de todas las frecuencias por hora/franja horaria y para cada día.

#bar_Formatter -- devuelvo el dataframe anterior formateado


def plot_barrios(barrios_elegidos):
    bsas_map = gpd.read_file('../../gopa_data/barrios-ciudad')
    puntos = gpd.GeoDataFrame(ciudad,
                             geometry = gpd.points_from_xy(ciudad.search_longitude, ciudad.search_latitude))

    fig,ax = plt.subplots(figsize = (10,10))
    bsas_map.plot(ax=ax, color='lightgrey')
    puntos[puntos['BARRIO'].isin(barrios_elegidos)].plot(ax=ax, markersize=5, color='red')
    ax.set_xlim([-58.550, -58.325])
    ax.set_ylim([-34.700, -34.525])
    plt.show()
    
def distribucion_por_dia(df, dia= None):    
    if dia == None:
        return df.hour.value_counts(normalize=True).sort_index()
    
    elif dia.lower() in df.weekday_name.unique():
        cond = df['weekday_name'] == dia
        return df[cond].hour.value_counts(normalize=True).sort_index()
    
    else:
        print('error, día no encontrado')

def agregador(columna, n): #columna a dividir, número de partición
    columna = columna.sort_index()
    valores = [ ( f'{i}-{i+n}' , sum(columna[i:i+n]) ) for i in range(0,24,n) ]
    return pd.DataFrame(valores,columns=['horario','probabilidad']).set_index('horario')

def plotear_dia(df, dia, n):
    data = distribucion_por_dia(df, dia)
    agregado = agregador(data,n) 
    x = agregado.index
    y = agregado.probabilidad
    plt.figure(figsize=(15,6))
    plt.bar(x ,y*100, color = 'lightgreen')
    plt.grid(lw=0.4)
    plt.ylabel('probabilidad', fontdict = {'size':20})
    plt.xlabel('Franja Horaria', fontdict = {'size':20})
    
    if n == 1:
        plt.title(f'Distribución de probabilidad cada 1 hora el día {dia.upper()}:\n{barrio_elegido[0]}', fontdict = {'size':25})
    else:
        plt.title(f'Distribución de probabilidad cada {n} horas el día {dia.upper()}:\n{barrio_elegido[0]}', fontdict = {'size':25})

    
    font = {'family': 'monospace' ,  'color':  'white',
            'size': 10, 'horizontalalignment':'center'}
    for i in range(24//n):
        plt.text(i, #x
                 y[i]*50,
                 f'{round(y[i]*100, 2)}%', 
                 fontdict=font,
                 path_effects=[pe.withStroke(linewidth=2, foreground="black")])

    plt.show()
    
    
def frecuencias_df(df=None,n_agregacion=1,con_semana=False): #dataframe, número de agregación horaria, agregarle columna con total semanal o no

    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

    if n_agregacion == 1:
        data = pd.DataFrame(index = np.arange(24))
        for i in dias_semana[0:]:
            data[i] = distribucion_por_dia(df, i)
            data[i].replace(np.nan, 0, inplace=True)
        #data.columns = dias_semana
        if con_semana == True:
            data['semana'] = distribucion_por_dia(df)
    
    else:
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        data = pd.DataFrame(index =  [f'{i}-{i+n_agregacion}' for i in range(0,24,n_agregacion)]  )
        for i in dias_semana:
            data[i] = agregador(distribucion_por_dia(df, i) , n_agregacion)
        data.columns = dias
        if con_semana == True:
            data['semana'] = agregador(distribucion_por_dia(df) , n_agregacion)
        
    return data

def bar_formatter(df):
    df_plot= df*100
    return df_plot.style.format(formatter='{:.3f}%').bar(color = 'lightgreen', vmax=df_plot.semana.max()*1.5,
                                                                  vmin = 0, 
                                                                  align = 'left',
                                                                  subset = 'semana')\
    .background_gradient(cmap = 'BuPu', subset = df.columns[0:-1],
                        low = 0, high = 4) 
    
bar_formatter(distribucion)