import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color me clean!")
        self.geometry("300x250")

        # Zmienne tkinter
        self.typ_wlosow_var = tk.StringVar()
        self.skora_glowy_var = tk.StringVar()
        self.porowatosc_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Typ włosów
        ttk.Label(self.master, text="Typ włosów:").pack(pady=5)
        ttk.Combobox(
            self.master,
            textvariable=self.typ_wlosow_var,
            values=["proste", "falowane", "kręcone"]
        ).pack()

        # Skóra głowy
        ttk.Label(self.master, text="Skóra głowy:").pack(pady=5)
        ttk.Combobox(
            self.master,
            textvariable=self.skora_glowy_var,
            values=["normalna", "sucha", "tłusta", "wrażliwa"]
        ).pack()

        # Porowatość
        ttk.Label(self.master, text="Porowatość włosów:").pack(pady=5)
        ttk.Combobox(
            self.master,
            textvariable=self.porowatosc_var,
            values=["niska", "średnia", "wysoka"]
        ).pack()

        # Przycisk
        ttk.Button(self.master, text="Zatwierdź", command=self.submit).pack(pady=20)

    def submit(self):
        typ = self.typ_wlosow_var.get()
        skora = self.skora_glowy_var.get()
        porowatosc = self.porowatosc_var.get()

        # Tutaj mógłbyś podpiąć model ML
        messagebox.showinfo(
            "Wybrane cechy",
            f"Typ włosów: {typ}\nSkóra głowy: {skora}\nPorowatość: {porowatosc}"
        )

if __name__ == "__main__":
    app = View()
    app.mainloop()
