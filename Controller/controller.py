import tkinter as tk
from tkinter import messagebox

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import random

from Other.utils import resource_path
from View.main import View
from Model.main import Model

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.view = view
        self.frame = view.frames['main_frame']

        self.model.ml_model.initialize_model()
        print(self.frame.typ_wlosow_var)
        self.frame.submit_button.config(command=self.handle_submit)

    def start(self):
        self.view.root.mainloop()
    
    
    def handle_submit(self):
        # Pobierz dane z GUI
        typ = self.view.typ_wlosow_var.get()
        skora = self.view.skora_glowy_var.get()
        porowatosc = self.view.porowatosc_var.get()

        if not all([typ, skora, porowatosc]):
            self.view.showerror("Błąd", "Wypełnij wszystkie pola!")
            return

        # Filtrowanie po pasujących cechach (jeśli kolumny nie są puste)
        filtered = self.df.copy()
        if 'typ_wlosow' in self.df.columns and typ:
            filtered = filtered[filtered['typ_wlosow'].fillna('').str.contains(typ, case=False, na=False)]
        if 'typ_skory' in self.df.columns and skora:
            filtered = filtered[filtered['typ_skory'].fillna('').str.contains(skora, case=False, na=False)]
        if 'porowatosc' in self.df.columns and porowatosc:
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
