import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from AnimatedGIF import AnimatedGIF


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color me clean!")
        self.geometry("420x420")
        self.background = "pink"
        self.configure(bg=self.background)

        # Zmienne tkinter
        self.typ_wlosow_var = tk.StringVar()
        self.skora_glowy_var = tk.StringVar()
        self.porowatosc_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # GIF
        gif = AnimatedGIF(self, 'hebe_360.gif', bg=self.background)
        gif.pack()
        # Typ włosów
        ttk.Label(self, text="Typ włosów:", background=self.background).pack(pady=5)
        ttk.Combobox(
            self,
            textvariable=self.typ_wlosow_var,
            values=["proste", "falowane", "kręcone"]
        ).pack()

        # Skóra głowy
        ttk.Label(self, text="Skóra głowy:", background=self.background).pack(pady=5)
        ttk.Combobox(
            self,
            textvariable=self.skora_glowy_var,
            values=["normalna", "sucha", "tłusta", "wrażliwa"]
        ).pack()

        # Porowatość
        ttk.Label(self, text="Porowatość włosów:", background=self.background).pack(pady=5)
        ttk.Combobox(
            self,
            textvariable=self.porowatosc_var,
            values=["niska", "średnia", "wysoka"]
        ).pack()

        # Przycisk
        ttk.Button(self, text="Zatwierdź", command=self.submit).pack(pady=20)

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
