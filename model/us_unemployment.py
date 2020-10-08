import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import folium

class Unemployment:
  unemployment_context = './model/data/us_unemployment.csv'
  us_map_json = './model/data/us_map.json'

  def __init__(self):
    pass

  def get_csv_data(self):
    unemploy_csv = pd.read_csv(self.unemployment_context, encoding='utf-8', thousands=',')
    return unemploy_csv

  def show_us_map(self):
    # usa_map = pd.read_json(self.us_map_json, encoding='utf-8')
    usa_map = json.load(open(self.us_map_json), encoding='utf-8')
    map = folium.Map(location=[37, -102], zoom_start=5)
    map.choropleth(
      geo_data=usa_map, 
      name = 'choropleth', 
      data=self.get_csv_data(),
      columns=['State', 'Unemployment'],
      key_on='feature.id',
      fill_color='YlGn',
      fill_opacity= 0.7,
      line_opacity= 0.2,
      legend_name = 'Unemployment Rate (%)'
    )
    folium.LayerControl().add_to(map)
    map.save('./model/data/usa.html')

if __name__ == "__main__":
    us = Unemployment()
    us.show_us_map()