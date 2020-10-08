import pandas as pd
import json

class FileReader:
    context: str = ''
    fname: str = ''
    train: object = None
    test: object = None
    id: str = ''
    label: str = ''

    def xls_to_dframe(self, header, usecols) -> object:
      return pd.read_excel(self.new_file(), encoding='utf-8', header=header)

    def json_load(self, file):
      return json.load(open(file), encoding='utf-8')