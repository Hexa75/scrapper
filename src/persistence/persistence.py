import os.path
import pandas as pd


class DataManager:

    def __init__(self):
        self.dir_path = 'data'

    def _make_file_path(self, company, max_pages):
        extension = '.csv'
        file_path = self.dir_path + '/' + company + '_' + str(max_pages) + extension
        return file_path

    def exists(self, company, max_pages):
        file_path = self._make_file_path(company, max_pages)
        return os.path.exists(file_path)

    def load(self, company, max_pages):
        file_path = self._make_file_path(company, max_pages)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col=[0])
            return df
        else:
            return None

    def save(self, df: pd.DataFrame, company: str, max_pages: int):
        file_path = self._make_file_path(company, max_pages)
        df.to_csv(file_path)



