import random, re, numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import pandas as pd


class HairRecommender:
    def __init__(self):
        self.df = pd.read_csv('../Data/CSV/produkty_hebe_raw.csv', index_col=0)
        self.preprocess()

    def clean_ingredients(self, text):
        # Twój kod - super!
        if pd.isna(text): return ""
        text = re.sub(r'[^\w\s,;/()]+', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s*\([^)]*\)', '', text)
        text = re.sub(r'^(ingredients|inci):\s*', '', text)
        return ', '.join([s.strip() for s in text.split(',') if s.strip()][:50])

    def preprocess(self):
        self.df['skladniki_clean'] = self.df['skladniki'].apply(self.clean_ingredients)

        # LOSOWE ETYKIETY (do pracy: ręczne!)
        self.df['typ_wlosow'] = [random.choice(['proste', 'falowane', 'krecone']) for _ in self.df.index]
        self.df['typ_skory'] = [random.choice(['normalna', 'sucha', 'tlusta', 'wrazliwa']) for _ in self.df.index]
        self.df['porowatosc'] = [random.choice(['niska', 'srednia', 'wysoka']) for _ in self.df.index]

        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self.model.encode(self.df['skladniki_clean'].tolist())

        # SPLIT dla przyszłego klasyfikatora
        X_train, X_test, y_train, y_test = train_test_split(
            self.embeddings, self.df[['typ_wlosow', 'typ_skory', 'porowatosc']],
            test_size=0.2, random_state=42
        )
        print(f"Embeddings shape: {self.embeddings.shape}")  # (2018, 384)

    def recommend_similar(self, product_id, top_k=10, typ_wlosow=None, typ_skory=None):
        """CORE: Content-based + filtr usera"""
        sim_scores = cosine_similarity([self.embeddings[product_id]], self.embeddings)[0]

        # Filtrowanie po preferencjach usera
        mask = np.ones(len(self.df), dtype=bool)
        if typ_wlosow:
            mask &= self.df['typ_wlosow'].str.contains(typ_wlosow, case=False, na=False)
        if typ_skory:
            mask &= self.df['typ_skory'].str.contains(typ_skory, case=False, na=False)

        sim_scores[~mask] = -1  # Ukryj niepasujące

        top_idx = np.argsort(sim_scores)[::-1][:top_k]
        recs = self.df.iloc[top_idx][['nazwa', 'cena', 'url', 'typ_wlosow', 'typ_skory']].reset_index(drop=True)
        recs['similarity'] = sim_scores[top_idx]
        return recs


if __name__ == '__main__':
    rec = HairRecommender()
    print(rec.recommend_similar(0, top_k=5, typ_wlosow='krecone'))  # Przykładowo
