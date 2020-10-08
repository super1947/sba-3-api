import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.file_helper import FileReader
basedir = os.path.dirname(os.path.abspath(__file__))
from model.SeoulCrime import SeoulCrime
from model.police import Police
import folium
import json
import googlemaps

class Crimemap:
  seoul_map_json = './model/data/seoul_map.json'

  def __init__(self):
    pass

  def hook_process(self):
    police = Police()
    police_norm = police.get_police_norm()
    self.create_seoul_crime_map()

  # def get_police_norm(self):
  #   get_police_norm = pd.read_csv('./model/data/police_norm.csv')
  #   # print(f'{get_police_norm.head()}')
  #   return get_police_norm

  def create_seoul_crime_map(self):
    crimemodel = SeoulCrime()
    crime = crimemodel.get_crime()
    police_norm = pd.read_csv('./model/data/police_norm.csv')
    station_names = []
    for name in crime['관서명']:
        station_names.append('서울'+str(name[:-1]+'경찰서'))
    station_addrs = []
    station_lats = [] # 위도
    station_lngs = [] # 경도
    gmaps = googlemaps.Client(key='')
    for name in station_names:
        t = gmaps.geocode(name, language='ko')
        station_addrs.append(t[0].get('formatted_address'))
        t_loc = t[0].get('geometry')
        station_lats.append(t_loc['location']['lat'])
        station_lngs.append(t_loc['location']['lng'])
        print(name+'---->' + t[0].get('formatted_address'))

    police_position = pd.read_csv('./model/data/police_position.csv', encoding='utf-8')
    police_position['lat'] = station_lats
    police_position['lngs'] = station_lngs

    print(police_position)

    col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
    tmp = police_position[col] / police_position[col].max() 
    police_position['검거'] = np.sum(tmp, axis=1)
  

    seoul_map = json.load(open(self.seoul_map_json, mode='rt', encoding='utf-8'))
    map = folium.Map(location=[37.5502, 126.982], zoom_start=12)
    map.choropleth(
      geo_data = seoul_map, 
      name = 'choropleth', 
      data = tuple(zip(police_norm['구별'], police_norm['범죄'])),
      columns=['구별', '살인검거율'],
      key_on='feature.id',
      fill_color='PuRd',
      fill_opacity= 0.7,
      line_opacity= 0.2,
      legend_name = '구별 살인 검거율 (%)'
    )
    folium.LayerControl().add_to(map)
    map.save('./model/data/seoul.html')

if __name__ == "__main__":
    crimemap = Crimemap()
    crimemap.hook_process()