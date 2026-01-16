from tkinter import messagebox
import pandas as pd
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

    def predict_full_cosmetic(self, ingredients: str) -> dict:
        emb = self.model.ml_model.embedding_model.encode([ingredients])
        emb_df = pd.DataFrame(emb, columns=[f"dim_{i}" for i in range(384)])

        # Cyfra → string przez classes_
        hair_idx = int(self.model.ml_model.hair_model.predict(emb_df)[0])
        skin_idx = int(self.model.ml_model.skin_model.predict(emb_df)[0])
        por_idx = int(self.model.ml_model.por_model.predict(emb_df)[0])

        return {
            "typ_wlosow": self.model.ml_model.hair_classes[hair_idx],
            "typ_skory": self.model.ml_model.skin_classes[skin_idx],
            "porowatosc": self.model.ml_model.por_classes[por_idx]
        }

    def handle_submit(self):
        user_hair = self.frame.typ_wlosow_var.get()
        user_skin = self.frame.skora_glowy_var.get()
        user_por = self.frame.porowatosc_var.get()
        ingredients = self.frame.ingredients_entry.get().strip()

        if not ingredients:
            messagebox.showwarning("Błąd", "Wpisz składniki!")
            return

        model_pred = self.predict_full_cosmetic(ingredients)

        hair_match = "✅" if model_pred["typ_wlosow"] == user_hair else "❌"
        skin_match = "✅" if model_pred["typ_skory"] == user_skin else "❌"
        por_match = "✅" if model_pred["porowatosc"] == user_por else "❌"

        matches = sum([hair_match == "✅", skin_match == "✅", por_match == "✅"])
        verdict = "🟢 IDEALNY" if matches == 3 else f"🟡 {matches}/3"

        messagebox.showinfo("Dopasowanie", f"""
    PREDYKCJA: {model_pred['typ_wlosow']} | {model_pred['typ_skory']} | {model_pred['porowatosc']}
    {model_pred['typ_wlosow']} ← {hair_match} {user_hair}
    {model_pred['typ_skory']} ← {skin_match} {user_skin}
    {model_pred['porowatosc']} ← {por_match} {user_por}

    {verdict}
        """)


if __name__ == '__main__':
    Controller()
