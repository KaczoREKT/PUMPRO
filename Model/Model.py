import random


from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class Model:
    def __init__(self):
        self.base_model = DecisionTreeClassifier
        self.model = MultiOutputClassifier(self.base_model(max_depth=10, criterion='gini', random_state=42))

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def get_accuracy(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    def get_prediction(self, X_test):
        return self.model.predict(X_test)


