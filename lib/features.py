#import data related libraries
import json
import pandas as pd
import numpy as np


#load states
with open('data/departamentos_col.json') as f:
    states_dict = json.loads(f.read())

def add_features(df):
    #dates
    df['Ingreso_Month'] = pd.to_datetime(df['fecha_ingreso'].map(lambda x: "{}-{}".format(x.year, x.month)))
    df['fecha_captura'] = pd.to_datetime(df['fecha_captura'], format = '%Y-%m-%d')
    df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], format = '%Y-%m-%d')
    df['fecha_salida'] = pd.to_datetime(df['fecha_salida'], format = '%Y-%m-%d')

    #recalculate age
    df['edad'] = (df['fecha_ingreso'] - pd.to_datetime(df['ano_nacimiento'] , format = '%Y' ))/np.timedelta64(1,'Y')

    #calculate sentencia
    df['sentencia'] = (df['fecha_salida'] - df['fecha_ingreso']) / np.timedelta64(1, 'Y')
    df['sentencia'] = df['sentencia'].apply(lambda x: x if x > 0 else np.nan)

    #ISO codes for departamentos
    df['depto_abr'] = df['depto_establecimiento'].map(states_dict)

    #add target for queries
    df['target'] = df['reincidente'].replace({0: 'Recidivist', 1: 'Nonrecidivist'})

    return df

