import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from Model.llm import OpenAILLM
from Other.utils import read_file


def clean_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizuje INCI do postaci: 'aqua, sodium laureth sulfate, ...'"""
    prompt = read_file("../Data/prompts/clean_text.txt")
    llm = OpenAILLM(prompt=prompt, model="gpt-4o-mini", stream=False)

    def transform_one(x):
        if pd.isna(x) or str(x).strip() == "":
            return ""
        return llm.generate_message(str(x))

    df['skladniki'] = df['skladniki'].apply(transform_one)
    return df


def encode_ingredients(
        df: pd.DataFrame,
        text_col: str = "skladniki",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        batch_size: int = 64,
) -> pd.DataFrame:
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(model_name, device=device)

    texts = df[text_col].fillna("").astype(str).tolist()
    print(f"Encoding {len(texts)} texts...")

    emb = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        device=device
    )

    emb_df = pd.DataFrame(emb, columns=[f"dim_{i}" for i in range(emb.shape[1])])
    df = pd.concat([df.reset_index(drop=True), emb_df], axis=1)

    return df


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    emb_cols = [col for col in df.columns if col.startswith("dim_")]
    X = df[emb_cols]
    y = df[['typ_wlosow', 'typ_skory', 'porowatosc_wlosow']]
    return X, y


def pipeline():
    df = pd.read_csv("CSV/produkty_hebe_clean.csv", sep=";")

    # Opcjonalnie: clean_ingredients(df)
    df = encode_ingredients(df)

    X, y = split_data(df)

    X.to_csv("CSV/features.csv", index=False)
    y.to_csv("CSV/labels.csv", index=False)

    print(f"X shape: {X.shape}, y shape: {y.shape}")

if __name__ == '__main__':
    df = pd.read_csv("CSV/produkty_hebe_clean.csv", sep=";")
    print(df['typ_wlosow'].value_counts())
    print(df['typ_skory'].value_counts())
    print(df['porowatosc_wlosow'].value_counts())

