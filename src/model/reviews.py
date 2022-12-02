from src.persistence.persistence import DataManager
from src.factory.scrapper import ReviewScrapper
from src.config import matching_rule


class Reviews:
    def __init__(self, company: str, max_pages: int):
        dm = DataManager()
        if dm.exists(company, max_pages):
            df = dm.load(company, max_pages)
        else:
            df = ReviewScrapper(company, max_pages).scrap_data()
            dm.save(df, company, max_pages)
        self.df = df

    def add_str_to_column(self, col: str, wrd=' '):
        self.df[col] = self.df[col] + wrd

    def add_columns(self, col_tg, *columns):
        self.df[col_tg] = ''
        for col in columns:
            self.df[col_tg] += (self.df[col] + '\n')

    def transform_rating(self, col_tg='str_ratings', col='ratings'):

        self.df[col_tg] = [matching_rule[str(key)] for key in list(self.df[col])]
