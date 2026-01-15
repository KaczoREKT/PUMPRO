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
        self.frame.submit_button.config(command=self.handle_submit)

    def start(self):
        self.view.root.mainloop()
    
    def handle_submit(self):
        typ = self.frame.typ_wlosow_var.get()
        skora = self.frame.skora_glowy_var.get()
        porowatosc = self.frame.porowatosc_var.get()

        if not all([typ, skora, porowatosc]):
            self.view.showerror("Błąd", "Wypełnij wszystkie pola!")
            return
        # znajdz najważniejszy składnik w wybranych
        top_ingredients, best_match = self.model.data.get_top_ingredients(typ, skora, porowatosc)
        if top_ingredients is None:
            self.view.showerror("Brak dopasowania", "Nie znaleziono pasujących produktów.")
            return
        # znajdz najlepszy szampon na podstawie top ingridients
        self.view.showinfo("Rekomendacja",
                            f"Zalecane składniki: {top_ingredients}\n"
                            f"Najlepiej dopasowany szampon: {best_match['nazwa']}")

if __name__ == '__main__':
    Controller()
