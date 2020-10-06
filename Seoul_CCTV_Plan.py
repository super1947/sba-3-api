'''
서울시에서 의뢰 
과거의 구별 CCTV 데이터를 줄테니, 
2018년 구별 CCTV 설치 수를 예측해 주세요.
1. 범죄율에 따른 최적화된 CCTV 수량 예측
2. 구별로 충분량, 부족량인지 판단해서 CCTV 할당량을 예측해주세요.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class SeoulCCTV:
  def __init__(self):
    self.CCTV = pd.read_csv('./data/cctv_in_seoul.csv', header=None)
    print(self.CCTV.head())
    print(self.CCTV.tail)
    print(self.CCTV.columns)


