import numpy as np
import pandas as pd


TRAINING_DATA_FILE_PATH = 'data/train.csv'
TESTING_DATA_FILE_PATH = 'data/test.csv'


class Model:
    def __init__(self):
        self.train_X = None
        pass

    def gradient_descent(self, iter=1000):
        pass

    def save(self):
        pass

    def load(self):
        pass


class Data:
    def __init__(self, path):
        self.df = pd.read_csv(path, encoding='big5').replace('NR', 0)
        self.feature = self._get_unique_feature()
        self.normalization()
        self.all_date = list(self.df['日期'].unique())
        self.all_month = {self._fetch_date_yyyymm(date) for date in self.all_date}
        self._group_data_by_month()

    def _fetch_samples(self):
        pass

    def _get_unique_feature(self):
        return list(self.df['測項'].unique())

    def normalization(self, trim_outlier=False):
        self.df['']
        pass

    def _fetch_date_yyyymm(self, date):
        return '/'.join(date.split('/')[: -1])

    def _group_data_by_month(self):
        res = {}
        for m in self.all_month:
            res[m] = self.df.loc[[d.startswith(m) for d in self.df['日期']]]
        return res

    def _group_data_by_date(self):
        res = {}
        for date in self.all_date:
            res[date] = self.df.loc[[d.startswith(date) for d in self.df['日期']]]
        return res

    def fetch_training_data(self):
        """ fetch first 20 days of month as training data set """
        return

    def fetch_testing_data(self):
        pass


Data(TRAINING_DATA_FILE_PATH)
