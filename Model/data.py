import random
from Other.utils import resource_path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

class Data:
    def __init__(self):
        self.df = pd.read_csv(resource_path('Data/produkty_hebe.csv'), index_col=0)
    
    def load_data(self):
        self.df['typ_wlosow'] = [random.choice(['proste', 'falowane', 'kręcone']) for _ in range(len(self.df))]
        self.df['typ_skory'] = [random.choice(['normalna', 'sucha', 'tłusta', 'wrażliwa']) for _ in range(len(self.df))]
        self.df['porowatosc'] = [random.choice(['niska', 'średnia', 'wysoka']) for _ in range(len(self.df))]

        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), binary=True)
        X = vectorizer.fit_transform(self.df['skladniki'])

        y = self.df[['typ_wlosow', 'typ_skory', 'porowatosc']]

        return train_test_split(X, y, test_size=0.2, random_state=42)