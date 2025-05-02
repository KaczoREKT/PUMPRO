import tkinter as tk
from tkinter import messagebox

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import random

from View.View import View
from Model.Model import Model

class Controller:
    def __init__(self):
        self.model = Model()
        self.feature_names = None

        # Załaduj dane i wytrenuj model
        self.X_train, self.X_test, self.y_train, self.y_test = self.load_data()
        self.model.train(self.X_train, self.y_train)

        # Inicjalizuj GUI
        self.view = View(self)
        self.view.submit = self.handle_submit
        self.view.mainloop()

    def load_data(self):
        self.df = pd.read_csv('Data/produkty_hebe.csv', index_col=0)

        # Dodaj brakujące kolumny (jeśli nie istnieją)
        self.df['typ_wlosow'] = [random.choice(['proste', 'falowane', 'kręcone']) for _ in range(len(self.df))]
        self.df['typ_skory'] = [random.choice(['normalna', 'sucha', 'tłusta', 'wrażliwa']) for _ in range(len(self.df))]
        self.df['porowatosc'] = [random.choice(['niska', 'średnia', 'wysoka']) for _ in range(len(self.df))]

        # Wektor składników (X)
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), binary=True)
        X = vectorizer.fit_transform(self.df['skladniki'])

        # Etykiety
        y = self.df[['typ_wlosow', 'typ_skory', 'porowatosc']]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def handle_submit(self):
        # Pobierz dane z GUI
        typ = self.view.typ_wlosow_var.get()
        skora = self.view.skora_glowy_var.get()
        porowatosc = self.view.porowatosc_var.get()

        if not all([typ, skora, porowatosc]):
            messagebox.showerror("Błąd", "Wypełnij wszystkie pola!")
            return

        # Wczytaj dane szamponów (np. wcześniej wczytany DataFrame przypisany do self.shampoo_df)
        df = self.df

        # Filtrowanie po pasujących cechach (jeśli kolumny nie są puste)
        filtered = df.copy()
        if 'typ_wlosow' in df.columns and typ:
            filtered = filtered[filtered['typ_wlosow'].fillna('').str.contains(typ, case=False, na=False)]
        if 'typ_skory' in df.columns and skora:
            filtered = filtered[filtered['typ_skory'].fillna('').str.contains(skora, case=False, na=False)]
        if 'porowatosc' in df.columns and porowatosc:
            filtered = filtered[filtered['porowatosc'].fillna('').str.contains(porowatosc, case=False, na=False)]

        if filtered.empty:
            messagebox.showinfo("Brak wyników", "Nie znaleziono pasujących szamponów.")
            return

        # Wybierz najlepiej dopasowany szampon - np. pierwszy z listy (lub można zastosować scoring)
        best_match = filtered.iloc[0]

        # Wyodrębnij składniki
        ingredients = best_match['skladniki'].split(',')
        top_ingredients = ', '.join([i.strip() for i in ingredients[:3]])

        # Wyświetl wynik
        messagebox.showinfo("Rekomendacja",
                            f"Zalecane składniki: {top_ingredients}\n"
                            f"Najlepiej dopasowany szampon: {best_match['nazwa']}")

if __name__ == '__main__':
    Controller()
