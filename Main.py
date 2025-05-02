from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import random
import pandas as pd

from Controller import Controller
from Model.Model import Model
from View.View import View


def load_and_split_data():
    # Wczytaj dane
    df = pd.read_csv('Data/produkty_hebe.csv', header=0, index_col=0)

    # Losowe dane dla typu skóry, włosów i ich porowatości.
    df['typ_wlosow'] = [random.choice(['kręcone', 'proste']) for _ in range(len(df))]
    df['typ_skory'] = [random.choice(['sucha', 'tłusta', 'normalna']) for _ in range(len(df))]
    df['porowatosc'] = [random.choice(['niska', 'średnia', 'wysoka']) for _ in range(len(df))]
    print(df.head())

    # Wektor składników (X)
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), binary=True)
    X = vectorizer.fit_transform(df['skladniki'])

    # Etykiety
    y = df[['typ_wlosow', 'typ_skory', 'porowatosc']]

    # Podział danych
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, vectorizer

if __name__ == '__main__':
    model = Model()
    controller = Controller()
    view = View(controller)
    X_train, X_test, y_train, y_test, vectorizer = load_and_split_data()
    model.train(X_train, y_train)
    print(f"Accuracy = {model.get_accuracy(X_test, y_test)}")

    # Przewidywanie dla przykładowego szamponu
    szampon_skladniki = "Aqua, Sodium Coco-Sulfate, Cocamidopropyl Betaine, Glycerin"
    X_szampon = vectorizer.transform([szampon_skladniki])

    predict = model.get_prediction(X_szampon)
    print(f"Dla {szampon_skladniki}:")
    print("Przewidywany typ włosów:", predict[0][0])
    print("Przewidywany typ skóry:", predict[0][1])
    print("Przewidywana porowatość:", predict[0][2])