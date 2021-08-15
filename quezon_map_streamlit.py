# -*- coding: utf-8 -*-
"""
Created on

@author: abegail
"""
# -*- coding: utf-8 -*-
"""
Created on Sun 

@author: abegail
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns 
from folium import Marker
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
import folium
from folium import Choropleth



from streamlit_folium import folium_static
import streamlit as st

st.set_page_config(layout="wide")

# Read the file
quezon = gpd.read_file(r"\quezon.geojson")


#use geocode
def getlatitude_longitude(name):
  #result = geocode(name, provider="nominatim")
  geolocator = Nominatim(user_agent="quezon_map_streamlit")
  result = geolocator.geocode(name)
  Latitude= result.latitude
  Longitude =result.longitude
  #point = result.geometry.iloc[0]
  #Latitude =  point.y
  #Longitude = point.x
  #print(str(Latitude) + " and " + str(Longitude))
  return Latitude , Longitude


quezon_pd= quezon.copy()

qname = quezon['NAME_2'][1] +","+quezon['PROVINCE'][1]
lat, longi = getlatitude_longitude(qname)
#print(lat)
#print(longi)


qlati = []
qlongi=[]
for idx , row in quezon.iterrows():
  #print(row['NAME_2'][idx])
  #print(idx)
  try: 
    qname = quezon['NAME_2'][idx] +","+quezon['PROVINCE'][idx]
    lat, longi = getlatitude_longitude(qname)
    qlati.append(lat)
    qlongi.append(longi)

  except:
    qname = quezon['NAME_2'][idx]
    lat, longi = getlatitude_longitude(qname)
    qlati.append(lat)
    qlongi.append(longi)


quezon_pd['Latitude'] = qlati
quezon_pd['Longitude'] = qlongi


quezon_pd['NumCases'] = quezon_pd['NumCases'].fillna(0)

quelat , quelong = getlatitude_longitude('Tayabas')
#print(str(quelat) + " and "+ str(qlongi))


#m = folium.Map(location=[quelat, quelong],zoom_start=10)

#for idx, row in quezon_pd.iterrows():
#  pop = 'Numcases: ' + str(quezon_pd['NumCases'][idx]) +'\n Hospital Available:  '
#  Marker([quezon_pd['Latitude'][idx],quezon_pd['Longitude'][idx]],popup=pop).add_to(m)

#m


m = folium.Map(location=[quelat, quelong], tiles='cartodbpositron', zoom_start=9)

#m_6 = folium.Map(location=[quelat, quelong], tiles='openstreetmap', zoom_start=12)

muni = quezon_pd[["geometry","NAME_2"]].set_index("NAME_2")
case= quezon_pd[["NumCases","NAME_2"]].set_index("NAME_2")
case=pd.DataFrame(case)

choice = ['NumCases','Active Cases', 'Cured/Discharged', 'Death']
choice_selected = st.selectbox("Select Choice ", choice)

# Add a choropleth map to the base map
Choropleth(geo_data=muni['geometry'].__geo_interface__, 
           data=case[choice_selected], key_on="feature.id", 
           fill_color='YlGnBu',legend_name='Quezon Number COVID Cases').add_to(m)

#m
folium_static(m, width=950, height=950)


