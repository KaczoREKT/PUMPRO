import tkinter as tk
from tkinter import messagebox
from .animated_gif import AnimatedGIF
from Other.utils import resource_path
from tkinter import ttk

class MainFrame(tk.Frame):
    def __init__(self, root):
        #utwórz main Frame
        super().__init__(root)
        self.background = "pink"
        self.configure(bg=self.background)
        
        self.typ_wlosow_var = tk.StringVar()
        self.skora_glowy_var = tk.StringVar()
        self.porowatosc_var = tk.StringVar()

        #GIF
        self.hebe_gif = AnimatedGIF(self)
        self.hebe_gif.pack()

        # pole wybrania typów włosów
        self.hair_type_label = ttk.Label(self, text="Typ włosów:", background=self.background)
        self.hair_type_label.pack(pady=5)
        self.hair_type_combobox = ttk.Combobox(
            self,
            textvariable=self.typ_wlosow_var,
            values=["normalne", "krecone/falowane", "puszace/suche"]
        )
        self.hair_type_combobox.pack()
        # pole wybrania skóry głowy
        self.skin_type_label = ttk.Label(self, text="Skóra głowy:", background=self.background)
        self.skin_type_label.pack(pady=5)
        self.skin_type_combobox = ttk.Combobox(
            self,
            textvariable=self.skora_glowy_var,
            values=["normalna", "tlusta/lupiez", "sucha/wrazliwa"]
        )
        self.skin_type_combobox.pack()
        self.porosity_type_label = ttk.Label(self, text="Porowatość włosów:", background=self.background)
        self.porosity_type_label.pack(pady=5)
        self.porosity_type_combobox = ttk.Combobox(
            self,
            textvariable=self.porowatosc_var,
            values=["niska", "srednia", "wysoka"]
        )
        self.porosity_type_combobox.pack()

        self.ingredients_label = ttk.Label(self, text="Wpisz składniki INCI (przecinki):", background=self.background)
        self.ingredients_label.pack(pady=5)
        self.ingredients_text = tk.Text(
            self,
            height=6,
            width=60,
            font=("Arial", 11),
        )
        self.ingredients_text.pack(pady=5)
        self.ingredients_text.insert(tk.END, "woda\ntruskawki\n")

        #przycisk zatwierdź wybór
        self.submit_button = ttk.Button(self, text="Zatwierdź")
        self.submit_button.pack(pady=20)

    def submit(self):
        typ = self.typ_wlosow_var.get()
        skora = self.skora_glowy_var.get()
        porowatosc = self.porowatosc_var.get()
        
        messagebox.showinfo(
            "Wybrane cechy",
            f"Typ włosów: {typ}\nSkóra głowy: {skora}\nPorowatość: {porowatosc}"
        )