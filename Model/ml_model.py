import random
import pickle
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
from Other.config import config
warnings.filterwarnings("ignore")

class MLModel:
    def __init__(self):
        self.model = None
        self.initialize_model()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def get_accuracy(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    def get_prediction(self, X_test):
        return self.model.predict(X_test)

    def create_model(self):
        base_model = DecisionTreeClassifier(**config['ml_model']['parameters'])
        self.model = MultiOutputClassifier(base_model)

    def load_model(self):
        try:
            with open(config['paths']['ml_model_path'], 'rb') as f:
                self.model = pickle.load(f)
        except Exception as e:
            return None
    
    def initialize_model(self):
        # utwórz i wytrenuj model na danych
        if config['paths']['ml_model_path']:
            self.load_model()
        else:
            self.create_model()
            self.train_model()
            
    