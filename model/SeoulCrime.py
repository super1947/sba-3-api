import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
import sys
import googlemaps
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class SeoulCrime:
  crime_context = './model/data/crime_in_seoul.csv'

  def __init__(self):
    pass

  def hook_process(self):
    print('----------------------- CRIME & POLICE -----------------------')
    crime = self.get_crime()
    self.get_station(crime)
    # self.get_crime_police()

  def get_crime(self):
    crime = pd.read_csv(self.crime_context, encoding='utf-8', thousands=',')
    # print(crime.head())
    # print(crime.columns)
    return crime

  # def create_gmaps(self):
  #   return googlemaps.Client(key='AIzaSyCnfFlHUWzghRMXTc_L-a3RrON1BekSFjA')

  def get_station(self, crime):
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
      gu_names = []
      for name in station_addrs:
          t = name.split()
          gu_name = [gu for gu in t if gu[-1] == '구'][0]
          gu_names.append(gu_name)
      crime['구별'] = gu_names
      print('+++++++++++++++++++++')
      
      crime.loc[crime['관서명'] == '혜화서', ['구별']] == '종로구'
      crime.loc[crime['관서명'] == '서부서', ['구별']] == '은평구'
      crime.loc[crime['관서명'] == '강서서', ['구별']] == '양천구'
      crime.loc[crime['관서명'] == '종암서', ['구별']] == '성북구'
      crime.loc[crime['관서명'] == '방배서', ['구별']] == '서초구'
      crime.loc[crime['관서명'] == '수서서', ['구별']] == '강남구'
      print(crime.head())

      crime.to_csv('./model/data/crime_police.csv')

  def get_crime_police(self):
    crime_police = pd.read_csv('./model/data/crime_police.csv')
    print(f'{crime_police.head()}')
    return crime_police

if __name__ == "__main__":
    crime = SeoulCrime()
    crime.hook_process()