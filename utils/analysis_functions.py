import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import variables as vrb

# Primero dividir las variables por tipo, usando la función que programamos en los ejercicios
def card_tipo(df,umbral_categoria = 1000, umbral_continua = 30):
    # Primera parte: Preparo el dataset con cardinalidades, % variación cardinalidad, y tipos
    df_temp = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad y porcentaje de variación de cardinalidad
    df_temp = df_temp.T # Como nos da los valores de las columnas en columnas, y quiero que estas sean filas, la traspongo
    df_temp = df_temp.rename(columns = {0: "Card", 1: "%_Card", 2: "Tipo"}) # Cambio el nombre de la transposición anterior para que tengan más sentido, y uso asignación en vez de inplace = True (esto es arbitrario para el tamaño de este dataset)

    # Corrección para cuando solo tengo un valor
    df_temp.loc[df_temp.Card == 1, "%_Card"] = 0.00

    # Creo la columna de sugerenica de tipo de variable, empiezo considerando todas categóricas pero podría haber empezado por cualquiera, siempre que adapte los filtros siguientes de forma correspondiente
    df_temp["tipo_sugerido"] = "Categorica"
    df_temp.loc[df_temp["Card"] == 2, "tipo_sugerido"] = "Binaria"
    df_temp.loc[df_temp["Card"] >= umbral_categoria, "tipo_sugerido"] = "Numerica discreta"
    df_temp.loc[df_temp["%_Card"] >= umbral_continua, "tipo_sugerido"] = "Numerica continua"
    # Ojo los filtros aplicados cumplen con el enunciado pero no siguen su orden y planteamiento

    return df_temp

def get_groupby_dataframe(df, count_column, items = 0, sort_column = vrb.GROUP_BY_COUNT_COLUMN, ascending = False):
    resultado = pd.DataFrame(df)
    resultado.reset_index(drop = False, inplace=True)
    resultado.rename(columns={count_column:vrb.GROUP_BY_COUNT_COLUMN}, inplace=True)
    if sort_column != "":
        resultado.sort_values(by=sort_column, ascending=ascending , inplace=True)
    if items > 0:
         resultado = resultado[:items]
    return resultado

def get_groupby_count(df, groupby_column, count_column, items = 0, sort_column = vrb.GROUP_BY_COUNT_COLUMN, ascending = False):
    return get_groupby_dataframe(df.groupby([groupby_column])[count_column].count(), count_column, items, sort_column, ascending)

def get_groupby_mean(df, groupby_column, count_column, items = 0, sort_column = vrb.GROUP_BY_COUNT_COLUMN, ascending = False):
    return get_groupby_dataframe(df.groupby([groupby_column])[count_column].mean(), count_column, items, sort_column, ascending)


def pinta_hist_categorica_numerica(df, cat_column, count_column, figsize=(), rotation=90):

    fsize = (10, 5)
    if len(figsize) == 2:
        fsize = figsize
    fig, axes = plt.subplots(1, 1, figsize=fsize)
    ax = axes
    sns.barplot(x=df[cat_column], y=df[count_column][:20], ax = ax, hue=df[cat_column], palette='viridis', legend = False)

    ax.set_ylabel(count_column)
    ax.set_title(f'Distribución')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=rotation)
                
    plt.tight_layout()
    plt.show()

def pinta_hist_count_categorica_numerica(df, groupby_column, count_column, items = 0, sort_column = vrb.GROUP_BY_COUNT_COLUMN, ascending = False, figsize=(), rotation=90):
     df_aux = get_groupby_count(df, groupby_column, count_column, items, sort_column, ascending)
     pinta_hist_categorica_numerica(df_aux, groupby_column, vrb.GROUP_BY_COUNT_COLUMN, figsize, rotation)

def pinta_hist_mean_categorica_numerica(df, groupby_column, count_column, items = 0, sort_column = vrb.GROUP_BY_COUNT_COLUMN, ascending = False, figsize=(), rotation=90):
     df_aux = get_groupby_mean(df, groupby_column, count_column, items, sort_column, ascending)
     pinta_hist_categorica_numerica(df_aux, groupby_column, vrb.GROUP_BY_COUNT_COLUMN, figsize, rotation)


def pinta_categorica_numerica_fecha(df, cat_column, date_column, num_column, dict_colors = {}, ylim=()):
    unique_categories = df[cat_column].unique()
    fig = plt.figure(figsize=(15,5))

    if len(ylim) == 2:
        plt.ylim(ylim)


    for c_value in unique_categories:
        df_aux = df.loc[df[cat_column] == c_value]
        df_groupby = get_groupby_mean(df_aux, date_column, num_column, sort_column=date_column, ascending=True)

        if c_value in dict_colors:
            plt.plot(df_groupby[date_column], df_groupby[vrb.GROUP_BY_COUNT_COLUMN], color = dict_colors[c_value])
        else:
            plt.plot(df_groupby[date_column], df_groupby[vrb.GROUP_BY_COUNT_COLUMN])
     

def show_info_categoricas(df, columns):
    asterisk_count = 10
    for col in columns:    
        #Pintamos la cabecera de la columna
        print ("*"* (asterisk_count*2 + len(col) + 2 ))
        print(("*" * asterisk_count) + f" {col} " + ("*" * asterisk_count))
        print("MODA", df[col].mode())
        print ("*"* (asterisk_count*2 + len(col) + 2 ))

        
        print()
        print()

def plot_categorica_numerica_histogram(df, cat_col, num_col, bins = "auto", kde = True):
        plt.figure(figsize=(10, 6))
        
        sns.histplot(df[num_col], kde=kde, bins = bins)
        
        plt.title(f'Histograma {cat_col}-{num_col}')
        plt.xlabel(num_col)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

        


