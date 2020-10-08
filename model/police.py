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
from sklearn import preprocessing

class Police:
  def __init__(self):
    pass

  def hook_process(self):
    print('----------------------- POLICE -----------------------')
    # self.create_crime_rate()
    self.get_police_norm()

  def create_crime_rate(self):
    crime = SeoulCrime()
    crime_police = crime.get_crime_police()
    police = pd.pivot_table(crime_police, index='구별', aggfunc=np.sum)
    print(f'{police.head()}')
    police['살인검거율'] = (police['살인 검거'] / police['살인 발생']) * 100
    police['강간검거율'] = (police['강간 검거'] / police['강간 발생']) * 100
    police['강도검거율'] = (police['강도 검거'] / police['강도 발생']) * 100
    police['절도검거율'] = (police['절도 검거'] / police['절도 발생']) * 100
    police['폭력검거율'] = (police['폭력 검거'] / police['폭력 발생']) * 100

    police.drop(["살인 검거","강간 검거","강도 검거","절도 검거", "폭력 검거"], axis=1)
    crime_rate_columns = ['살인검거율', '강간검거율', '강도검거율', '절도검거율','폭력검거율']

    for i in crime_rate_columns:
      police.loc[police[i] > 100, 1] = 100
      police.rename(columns = {
        '살인 발생' : '살인',
        '강간 발생' : '강간',
        '강도 발생' : '강도',
        '절도 발생' : '절도',
        '폭력 발생' : '폭력'
      }, inplace=True)
      crime_columns = ['살인', '강간', '강도', '절도', '폭력']
      x = police[crime_rate_columns].values
      min_max_scalar = preprocessing.MinMaxScaler() # 정규화, 평균은 0, 분산은 1
      x_scaled = min_max_scalar.fit_transform(x.astype(float))
      police_norm = pd.DataFrame(x_scaled, columns=crime_columns, index=police.index)
      police_norm[crime_rate_columns] = police[crime_rate_columns]
      self.get_cctv_pop()
      police_norm['범죄'] = np.sum(police_norm[crime_rate_columns], axis=1)
      police_norm['검거'] = np.sum(police_norm[crime_columns], axis=1)
      police_norm.to_csv('./model/data/police_norm.csv', sep=',', encoding='utf-8')

  def get_cctv_pop(self):
    cctv_pop = pd.read_csv('./model/data/cctv_pop.csv', sep=',', index_col='구별')
    print(f'{cctv_pop.head()}')
    return cctv_pop

  def get_police_norm(self):
    get_police_norm = pd.read_csv('./model/data/police_norm.csv')
    print(f'{get_police_norm.head()}')
    return get_police_norm

if __name__ == "__main__":
    police = Police()
    police.hook_process()
