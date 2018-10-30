import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize


TRAINING_DATA_FILE_PATH = 'data/train.csv'
TESTING_DATA_FILE_PATH = 'data/test.csv'


class LinearModel:
    def __init__(self, X):
        pass

    def predict(self):
        pass

    def gradient_decent(self):
        pass

    def loss(self):
        pass


class Data:
    def __init__(self):
        pass

    def get_sample_point(self):
        pass

class TrainingData:
    def __init__(self, fp, k):
        # fetch raw data without first row (title)
        self.df = pd.read_csv(fp, encoding='big5', header=0).replace('NR', 0)
        self.k = k
        self.num_row = len(self.df)
        self.all_features = self._get_unique_feature()
        self.num_feature = len(self.all_features)

    def _get_unique_feature(self):
        return list(self.df['測項'].unique())

    def get_sample_point(self):
        data = None
        for i, one_day in enumerate(self.fetch_by_day()):
            if i == 0:
                data = one_day
            else:
                data = np.concatenate((data, one_day), axis=1)

        for i in range(len(data[0]) // self.k):
            pos = i * self.k
            yield data[:, pos: pos + self.k - 1], data[:, self.k]

    def fetch_by_day(self):
        for i in range(self.num_row // self.num_feature):
            day_start = i * self.num_feature
            yield self.df.loc[day_start: (day_start + self.num_feature - 1), '0': '23'].values


train_data = DataSet(TRAINING_DATA_FILE_PATH, 10)
# test_data = DataSet(TESTING_DATA_FILE_PATH)
