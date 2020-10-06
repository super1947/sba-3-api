import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.file_helper import FileReader
basedir = os.path.dirname(os.path.abspath(__file__))

class SeoulCCTV:
  cctv_context = './model/data/cctv_in_seoul.csv'
  pop_context = './model/data/pop_in_seoul.xls'

  def __init__(self):
    pass

  def hook_process(self):
    print('------------------ CCTV & POP ----------------------')
    cctv = self.get_cctv()
    pop = self.get_pop()
    # print(f'CCTV null Checker: {cctv["구별"].isnull()}')
    # print(f'CCTV Header: {cctv.head()}')
    # print(f'POP null Checker: {pop["구별"].isnull()}')
    # print(f'POP Header: {pop.head()}')
    self.show_corrcoef(pop, cctv)

  def get_cctv(self):
    cctv = pd.read_csv(self.cctv_context)
    # print(self.cctv.head())
    # print(self.cctv.tail)
    # print(self.cctv.columns)
    cctv.rename(columns = {cctv.columns[0]: '구별'}, inplace=True)
    return cctv

  def get_pop(self):
    pop = pd.read_excel(self.pop_context, header=2, usecols='B,D,G,J,N')
    # print(pop)
    pop.rename(columns = {
      pop.columns[0]: '구별',
      pop.columns[1]: '인구수',
      pop.columns[2]: '한국인',
      pop.columns[3]: '외국인',
      pop.columns[4]: '고령자'}, inplace=True)
    return pop


  def show_corrcoef(self, pop, cctv):
    pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
    pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100
    cctv.drop(["2013년도 이전","2014년","2015년","2016년"], 1, inplace=True)
    cctv_pop = pd.merge(cctv, pop, on='구별')
    cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
    cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
    print(f'고령자비율과 CCTV 의 상관계수 {cor1}')
    print(f'외국인비율과 CCTV 의 상관계수 {cor2}')

    cctv_pop.to_csv('./model/data/cctv_pop.csv')



if __name__ == "__main__":
    model = SeoulCCTV()
    model.hook_process()
