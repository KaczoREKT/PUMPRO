import random
import re

from sentence_transformers import SentenceTransformer

from Other.utils import resource_path
import pandas as pd
from sklearn.model_selection import train_test_split

class Data:
    def __init__(self):
        self.df = pd.read_csv(resource_path('../Data/CSV/produkty_hebe_transformed.csv'), index_col=0)

    def preprocess(self):
        # Przygotowanie danych 
        self.df['typ_wlosow'] = [random.choice(['proste', 'falowane', 'kręcone']) for _ in range(len(self.df))]
        self.df['typ_skory'] = [random.choice(['normalna', 'sucha', 'tłusta', 'wrażliwa']) for _ in range(len(self.df))]
        self.df['porowatosc'] = [random.choice(['niska', 'średnia', 'wysoka']) for _ in range(len(self.df))]

        self.df['skladniki_clean'] = self.df['skladniki'].apply(self.clean_ingredients)
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # multilingual dla PL
        X = model.encode(self.df['skladniki_clean'])
        y = self.df[['typ_wlosow', 'typ_skory', 'porowatosc']]

        return train_test_split(X, y, test_size=0.2, random_state=42)


    def get_top_ingredients(self, typ, skora, porowatosc, top_n=5):
        filtered = self.df.copy()
        if 'typ_wlosow' in self.df.columns and typ:
            filtered = filtered[filtered['typ_wlosow'].fillna('').str.contains(typ, case=False, na=False)]
        if 'typ_skory' in self.df.columns and skora:
            filtered = filtered[filtered['typ_skory'].fillna('').str.contains(skora, case=False, na=False)]
        if 'porowatosc' in self.df.columns and porowatosc:
            filtered = filtered[filtered['porowatosc'].fillna('').str.contains(porowatosc, case=False, na=False)]

        if filtered.empty:
            return None, None

        best_match = filtered.iloc[0]

        ingredients = best_match['skladniki'].split(',')
        top_ingredients = ', '.join([i.strip() for i in ingredients[:3]])
        return top_ingredients, best_match

if __name__ == '__main__':
    data = Data()
    for i in range(len(data.df['skladniki'])):
        print(data.df.iloc[i]['skladniki'])