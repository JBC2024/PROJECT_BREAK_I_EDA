import numpy as np
import pandas as pd
import variables as vrb
from functools import reduce

# Creamos esta función para transformar los valores de columnas categoricas con ids, a su correspondiente valor en texto
# Se le pasa como parámetro un diccionario que tendrá una clave y valor en formato texto
def get_value_from_dict(dict, val):
    resultado = vrb.VALUE_SIN_DETERMINAR
    key = str(val)
    if type(val) is float:
         key = str(int(val))
    key = key.replace(".0","")
    if key in dict.keys():
        resultado = dict[key]
    return resultado

# Función que sustituye los valores de una columna, que contiene identificadores, al texto correspondiente en su tabla maestra establecida en el diccionario
def replace_values_from_master(df, ref_column, dict):
    df[ref_column] = df[ref_column].apply( lambda x: get_value_from_dict(dict, x) )

# Función para completar los valores nulos de una columna a un valor por defecto
def fillna(df, ref_column, null_value):
    df.fillna({ref_column: null_value}, inplace=True)

# Funcion que rellena los nulos de una columna con 'null_value' y luego reemplaza los identificadores por el valor correspondiente en el diccionario que tiene los datos maestros
def fillna_and_replace_values_from_master(df, ref_column, dict, null_value):
    fillna(df, ref_column, null_value)
    replace_values_from_master(df, ref_column, dict)


# Funcion que establece, para los valores nulos, el valor de la moda de las columnas especificadas en "master_columns"
# Para las condiciones de agrupación, de cara a sacar la moda, se buscan valores que no contengan "X" (VALUE_SIN_DETERMINAR de variables)
def findby_master_columns(row, df, ref_column, master_columns, default_value):
    
    resultado = default_value

    valid_key = True
    idx = 0
    while valid_key and idx < len(master_columns):
        if master_columns[idx] != ref_column:
            valid_key = row[master_columns[idx]] != vrb.VALUE_SIN_DETERMINAR
        idx += 1
    if valid_key:
        cond_list = []
        for m_col in master_columns:
            cond_list.append(df[m_col] == row[m_col])

        valor = df.loc[reduce(np.logical_and, cond_list)][ref_column].tolist()
        #print("Valor:",valor)
        if len(valor) > 0:
            resultado = valor[0]

    return resultado

# Completa los valores nulos a partir de los valores de referencia indicados por master_columns. En el caso de que no haya valores, pone el valor por defecto "default_value"
def replace_null_from_master_columns(df, ref_column, master_columns, default_value, new_column = False, print_result = False):
    
    print(f"Estableciendo mmoda del campo '{ref_column}' para las columnas {master_columns}")

    columns = master_columns.copy()
    columns.append(ref_column)

    # De las columnas que no tienen nulos, generamos un dataframe que identifique la moda de la columna "ref_column" a partir de las claves maestras "master_columns"
    cond_list = []
    cond_list.append(df[ref_column].notna())
    for col in master_columns:
        cond_list.append(df[col] != vrb.VALUE_SIN_DETERMINAR)
    df_groupby = pd.DataFrame(df.loc[reduce(np.logical_and, cond_list)].groupby(master_columns)[ref_column].agg( lambda x: pd.Series.mode(x)[0] ))
    df_groupby.reset_index(inplace=True)

    #df_groupby.to_csv(vrb.SOURCE_DATA_BASE_PATH + f"MASTER_{ref_column}.csv")
    #display(df_groupby)

    #Establecemos el nombre de la columna a la que se asignarán los valores. Si new_column = True, añadimos el prefijo "_NEW" a "column_ref" para que cree una nueva columna
    set_column = ref_column
    if new_column:
        set_column += "_NEW"
    df.loc[df[ref_column].isna(), set_column] = df.loc[df[ref_column].isna(),columns].apply(findby_master_columns, axis = 1, args=(df_groupby, ref_column, master_columns, default_value,))

    if (print_result):
        columns.append(set_column)
        print("*"*35 + " RESULTADO " + "*"*35)
        display(df.loc[df[ref_column].isna()][columns])