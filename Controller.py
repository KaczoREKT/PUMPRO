import tkinter as tk
from tkinter import messagebox

from sklearn.model_selection import train_test_split
from View.View import View  # zakładam, że klasę View zapisałeś w osobnym pliku view.py
from Model.Model import Model  # zakładam, że klasę Model zapisałeś w model.py
import pandas as pd
import random

class Controller:
    def __init__(self):
        # Załaduj model
        self.model = Model()
        self.feature_names = None

        # Przygotuj dane
        self.X_train, self.X_test, self.y_train, self.y_test = self.load_data()
        self.model.train(self.X_train, self.y_train)

        # Inicjalizuj widok
        self.view = View()
        self.view.submit = self.handle_submit  # Przypisz funkcję obsługującą przycisk
        self.view.mainloop()

    def load_data(self):
        df = pd.read_csv('Data/produkty_hebe.csv', index_col=0)

        # Dodajemy sztuczne cechy, jeśli ich nie ma
        if 'typ_wlosow' not in df.columns:
            df['typ_wlosow'] = [random.choice(['proste', 'falowane', 'kręcone']) for _ in range(len(df))]
        if 'typ_skory' not in df.columns:
            df['typ_skory'] = [random.choice(['normalna', 'sucha', 'tłusta', 'wrażliwa']) for _ in range(len(df))]
        if 'porowatosc' not in df.columns:
            df['porowatosc'] = [random.choice(['niska', 'średnia', 'wysoka']) for _ in range(len(df))]

        X = df[['typ_wlosow', 'typ_skory', 'porowatosc']]
        y = df[['skladniki']]

        X_encoded = pd.get_dummies(X)
        self.feature_names = X_encoded.columns
        return train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    def handle_submit(self):
        # Pobierz dane z GUI
        typ = self.view.typ_wlosow_var.get()
        skora = self.view.skora_glowy_var.get()
        porowatosc = self.view.porowatosc_var.get()

        if not all([typ, skora, porowatosc]):
            messagebox.showerror("Błąd", "Wypełnij wszystkie pola!")
            return

        # Utwórz DataFrame i zakoduj
        X_input = pd.DataFrame([[typ, skora, porowatosc]], columns=['typ_wlosow', 'typ_skory', 'porowatosc'])
        X_input_encoded = pd.get_dummies(X_input)

        # Upewnij się, że kolumny są takie same jak przy treningu
        X_input_encoded = X_input_encoded.reindex(columns=self.feature_names, fill_value=0)

        # Przewiduj
        prediction = self.model.get_prediction(X_input_encoded)

        # Pokaż wynik
        messagebox.showinfo("Rekomendowany szampon", f"Zalecane składniki: {prediction[0][0]}")

if __name__ == '__main__':
    Controller()
