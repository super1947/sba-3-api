import pandas as pd

class FileReader:
    context: str = ''
    fname: str = ''
    train: object = None
    test: object = None
    id: str = ''
    label: str = ''

    def xls_to_dframe(self) -> object:
      return pd.read_excel()