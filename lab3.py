#ZENATI Mohamed TP 2


import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import plotly_express as px
import datetime as dt
from streamlit.elements.color_picker import ColorPickerMixin
import plotly_express as px
import seaborn as sns
import time
import os
import streamlit.components.v1 as components
from functools import wraps


st.title("ZENATI Mohamed TP 2")

df1 = pd.read_csv(("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/uber-raw-data-apr14.csv"))
df1['Date/Time']=pd.to_datetime(df1["Date/Time"])
df2=pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/ny-trips-data.csv")

def log_time(func):
    """
    Mesure le temps d'exécution d'une fonction.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        variable = "Durée d'exécution : {:1.3}s".format(end_time - start_time)
        file = open("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/tp3/monfichiertext.txt", "w") 
        file.write(variable) 
        file.close()
        
    return wrapper


components.html("""
<link href="https://unpkg.com/tailwindcss@%5E2/dist/tailwind.min.css" rel="stylesheet">
<div class="max-w-sm rounded overflow-hidden shadow-lg mx-auto my-8">
    <img class="w-full" src="https://www.letudiant.fr/static/uploads/mediatheque/ETU_ETU/4/4/2241244-adobestock-34019801-766x438.jpeg" alt="Sunset in the mountains">
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">Vive la data</div>
      <p class="text-gray-600 text-base">
        Voici mon premier dashboard de deux datasets
      </p>
    </div>
    <div class="px-6 py-4">
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-gray-600 mr-2">#JeMérite20/20</span>
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-gray-600 mr-2">#ViveStreamlit</span>
      
    </div>
  </div>
      </div>
    """,
    height=600,

)

def count_rows(rows):
    return len(rows)
def get_dom(dt):
    return dt.day
def get_weekday(dt):
    return dt.weekday()
def get_hour(dt):
    return dt.hour
def count_rows(rows):
    return len(rows)


def run_the_app():
    @st.cache
    def load_metadata(url):
        return pd.read_csv(url)


st.sidebar.title("Sélectionnez votre DataSet !")
app_mode = st.sidebar.selectbox("",
        ["uber-raw-data-apr14", "ny-trips-data"])

#@st.cache(allow_output_mutation=True) 
#@st.cache(suppress_st_warning=True)
#@log_time
def csv(app_mode):
    
    if app_mode== "uber-raw-data-apr14":
        st.sidebar.success('')
        run_the_app()
        df = pd.read_csv(("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/uber-raw-data-apr14.csv"))
        df['Date/Time']=pd.to_datetime(df["Date/Time"])
        df['day'] = df['Date/Time'].map(get_dom)
        df['weekday']= df['Date/Time'].map(get_weekday)
        df['hour'] = df['Date/Time'].map(get_hour)
        #by_date = df.groupby('day').apply(count_rows)

        df3 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()

        select_dataframe = st.sidebar.radio("Choisissez un histogramme", ('Par heure de la journée','Par jour de la semaine',
        'Par jour du mois', 'En carte et par heure','entre deux dates choisies','HeatMap','La totalité sur une carte'))
        select_dataframe_function(select_dataframe,df,df3)
    if app_mode=="ny-trips-data":
        st.sidebar.success('')
        run_the_app()
        st.title("Vous voila dans le DataSet suivant : ny-trips-data")
        
        df = pd.read_csv(("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/ny-trips-data.csv"))
        df['tpep_pickup_datetime']=pd.to_datetime(df["tpep_pickup_datetime"])
        df['tpep_dropoff_datetime']=pd.to_datetime(df["tpep_dropoff_datetime"])
        df['hour_pickup'] = df['tpep_pickup_datetime'].map(get_hour)
        df['hour_dropoff'] = df['tpep_dropoff_datetime'].map(get_hour)
        #st.write(df.head(10))

        select_dataframe = st.sidebar.radio("Choisissez un histogramme", ('Frequency of pickups per hour','All pickups in one map',
        'Frequency of dropoffs per hour','All dropoffs in one map','All pickups and dropoffs in one map'))
        select_dataframe_function2(select_dataframe,df)

#@st.cache(allow_output_mutation=True) 
@log_time
def select_dataframe_function(histogram,df,df3):
    if histogram=='Par heure de la journée':
        st.title('Fréquence de commande Uber par heures de la journée')
        fighour(df,df.hour)

    if histogram=='Par jour de la semaine':
        st.title('Fréquence de commande Uber par jour de la semaine')
        figweekday(df,df.weekday)
    if histogram=='Par jour du mois':
        st.title('Fréquence de commande Uber par jour du mois')
        figday(df,df.day)
        
    if histogram=='En carte et par heure':
        st.title('localisation des commande Uber par heures')
        hour_to_filter=st.slider('Select the hour',min_value=min(df['hour']),max_value=max(df['hour']))
        st.write("Slider:",hour_to_filter) 
        filtered_data = df[df["Date/Time"].dt.hour == hour_to_filter]
        st.subheader(f'Map des courses à {hour_to_filter}:00')
        filtered_data['lat'] = df['Lat']
        filtered_data['lon'] = df['Lon']
        st.map(filtered_data)
    if histogram=='Entre deux dates choisies':
        header_1_column, header_2_column, header_3_column = st.columns(3)

        date_debut = header_1_column.date_input(
            "Date début",
            dt.date(2014, 4, 1))

        date_fin = header_2_column.date_input(
            "Date fin",
            dt.date(2014, 4, 30))

        clique = header_3_column.button(
                'Rechercher les courses entre la date de début et la date de fin')

        if clique:
            mask = (df['Date/Time'].dt.date > date_debut) & (df['Date/Time'].dt.date <= date_fin)
            df = df.loc[mask]
            df.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
            st.map(df)
    
    if histogram=='HeatMap':
        st.title('Fréquence de commande Uber par jour de la semaine en heatmap')
        fig, ax = plt.subplots()
        sns.heatmap(df3, ax=ax)
        st.write(fig)
    if histogram=='La totalité sur une carte':
        st.title('Affichage sur une carte')
        fig, ax = plt.subplots()
        ax.plot(df.Lon, df.Lat, '.', ms = 2, alpha = .5)
        plt.xlim(-74.2, -73.7)
        plt.ylim(40.7, 41)
        plt.grid()
        st.write(fig)

#@st.cache(allow_output_mutation=True) 
@log_time
def select_dataframe_function2(histogram,df):
    if histogram=="Frequency of pickups per hour":
        st.title('Fréquence des pickups par heures')
        fighour(df,df.hour_pickup)

    if histogram=="All pickups in one map":
        st.title('Affichage sur une carte')
        fig, ax = plt.subplots()
        ax.plot(df.pickup_longitude, df.pickup_latitude, '.', ms = 2, alpha = .5)
        plt.xlim(-74.05, -73.75)
        plt.ylim(40.6, 40.98)
        plt.title('All pickups in one map')
        plt.grid()
        st.write(fig)
    if histogram=="Frequency of dropoffs per hour":
        st.title('Fréquence des dropoffs par heures')
        fighour(df,df.hour_dropoff)
    if histogram=="All dropoffs in one map":
        fig, ax = plt.subplots()
        ax.plot(df.dropoff_longitude, df.dropoff_latitude, '.', ms = 2, alpha = .5)
        plt.xlim(-74.05, -73.75)
        plt.ylim(40.6, 40.98)
        plt.title('All dropoffs in one map')
        plt.grid()
        st.write(fig)
    if histogram=='All pickups and dropoffs in one map':
        st.title('All pickups and dropoffs in one map')
        fig, ax = plt.subplots()
        plt.plot(df.dropoff_longitude, df.dropoff_latitude, '.', ms = 2, alpha = .5, color = 'r', label = 'dropoff')
        plt.plot(df.pickup_longitude, df.pickup_latitude, '.', ms = 2, alpha = .5, color = 'b', label = 'pickup')
        plt.xlim(-74.05, -73.75)
        plt.ylim(40.6, 40.98)
        plt.grid()
        st.write(fig)

def fighour(df,column):
    fig,ax=plt.subplots()
    plt.hist(column,bins=24,range=(0.5,24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    st.pyplot(fig)

def figweekday(df,column):
    fig, ax = plt.subplots()
    ax.hist(column, bins = 7, rwidth = 0.8, range = (-0.5, 6.5))
    plt.xlabel('Day of the week')
    plt.ylabel('Frequency')
    st.pyplot(fig)

def figday(df,column):
    fig, ax = plt.subplots()
    ax.hist(column, bins = 30, rwidth = 0.8, range = (0.5, 30.5))
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    st.pyplot(fig)

csv(app_mode)










