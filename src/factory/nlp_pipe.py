from transformers import pipeline
from src.config import labels
import pandas as pd


class NlpPipeline:

    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def run(self, complete_reviews: [str]):
        results = [self.classifier(cr, labels, multilabel=True) for cr in complete_reviews[:3]]
        # results = self.classifier(complete_reviews[:5], labels, multilabel=True)

        result = results[0]

        _sequence = result['sequence']
        _labels = result['labels']
        _scores = result['scores']

        result = {'review': _sequence}
        result.update({l:s for l,s in zip(_labels, _scores)})

        result = pd.DataFrame.from_dict([result])
        return result


