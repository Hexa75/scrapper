from src.factory.nlp_pipe import NlpPipeline
from src.model.reviews import Reviews


class Control:

    def __init__(self, company: str, max_pages: int):
        self.reviews = Reviews(company, max_pages)

    def _prepare(self):
        self.reviews.transform_rating('str_ratings', 'ratings')
        self.reviews.add_columns('complete_reviews', 'titles', 'str_ratings', 'reviews')

    def run(self):
        self._prepare()
        classifications = NlpPipeline().run(self.reviews.df['complete_reviews'])
        return self.reviews.df, classifications
