import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# Wczytaj dane
df = pd.read_csv('../Data/produkty_hebe.csv', header=0, index_col=0)

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

# Model ML
model = MultiOutputClassifier(DecisionTreeClassifier(max_depth=10, criterion='gini', random_state=42))
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("Dokładność:", accuracy)

# Przewidywanie dla przykładowego szamponu
szampon_skladniki = "Aqua, Sodium Coco-Sulfate, Cocamidopropyl Betaine, Glycerin"
X_szampon = vectorizer.transform([szampon_skladniki])

predict = model.predict(X_szampon)
print(f"Dla {szampon_skladniki}:")
print("Przewidywany typ włosów:", predict[0][0])
print("Przewidywany typ skóry:", predict[0][1])
print("Przewidywana porowatość:", predict[0][2])
