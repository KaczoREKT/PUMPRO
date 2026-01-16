import pickle
from sklearn.ensemble import RandomForestClassifier

def train_hair_type_classifier(embeddings_csv="CSV/features.csv",
                               labels_csv="CSV/labels.csv"):
    X = pd.read_csv(embeddings_csv)
    y_df = pd.read_csv(labels_csv)

    y = y_df['typ_wlosow'].values  # Target

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    with open('Models/hair_type_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    rf.fit(X_train, y_train)

    with open('Models/hair_type_classifier.pkl', 'wb') as f:
        pickle.dump(rf, f)

    y_pred = rf.predict(X_test)
    y_pred_proba = rf.predict_proba(X_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
    print(f"ROC AUC: {auc:.3f}")

    cv_scores = cross_val_score(rf, X, y_encoded, cv=5, scoring='accuracy')
    print(f"CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False).head(20)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=importances, x='importance', y='feature')
    plt.title("Top 20 Embedding Dimensions - Hair Type Classifier")
    plt.tight_layout()
    plt.savefig("hair_type_importance.png")
    plt.show()

    return rf, le, auc

def train_skin_type_classifier(embeddings_csv="CSV/features.csv",
                               labels_csv="CSV/labels.csv"):
    X = pd.read_csv(embeddings_csv)
    y_df = pd.read_csv(labels_csv)
    y = y_df['typ_skory'].values

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    with open('Models/skin_type_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=0.2, random_state=42, stratify=y_encoded
    )

    lr = LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver='saga',
        random_state=42,
        n_jobs=-1
    )

    lr.fit(X_train, y_train)

    with open('Models/skin_type_classifier.pkl', 'wb') as f:
        pickle.dump(lr, f)

    y_pred = lr.predict(X_test)
    y_pred_proba = lr.predict_proba(X_test)

    print("Classification Report (Typ skóry):")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
    print(f"ROC AUC: {auc:.3f}")

    cv_scores = cross_val_score(lr, X, y_encoded, cv=5, scoring='accuracy')
    print(f"CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    weights_df = pd.DataFrame({
        'dimension': X.columns,
        'weight_sucha': lr.coef_[0],
        'weight_tlusta': lr.coef_[1],
    })

    # Top wagi dla każdej klasy
    print("\nTop 10 wymiarów dla 'SUCHA':")
    print(weights_df.nlargest(10, 'weight_sucha')[['dimension', 'weight_sucha']])

    # Wizualizacja wag
    top_weights = weights_df.nlargest(20, 'weight_sucha')
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_weights, x='weight_sucha', y='dimension')
    plt.title("Top Embedding Dimensions dla Typu Skóry 'SUCHA' (Logistic Regression)")
    plt.tight_layout()
    plt.savefig("skin_type_weights.png", dpi=300)
    plt.show()

    return lr, le, auc


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


def train_porosity_classifier(embeddings_csv="CSV/features.csv",
                              labels_csv="CSV/labels.csv"):
    X = pd.read_csv(embeddings_csv)
    y_df = pd.read_csv(labels_csv)
    y = y_df['porowatosc_wlosow'].values

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    with open('Models/porosity_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    lr = LogisticRegression(
        C=1.5,
        max_iter=1000,
        solver='saga',
        random_state=42,
        n_jobs=-1
    )

    # Trening
    lr.fit(X_train, y_train)

    with open('Models/porosity_classifier.pkl', 'wb') as f:
        pickle.dump(lr, f)

    # Predykcje
    y_pred = lr.predict(X_test)
    y_pred_proba = lr.predict_proba(X_test)

    # Metryki
    print("Classification Report (Porowatość włosów):")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
    print(f"ROC AUC: {auc:.3f}")

    cv_scores = cross_val_score(lr, X, y_encoded, cv=5, scoring='accuracy')
    print(f"CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Wagi modelu (interpretacja)
    weights_df = pd.DataFrame({
        'dimension': X.columns,
        'weight_niska': lr.coef_[0],
        'weight_srednia': lr.coef_[1],
        'weight_wysoka': lr.coef_[2]
    })

    print("\nTop 10 dla 'WYSOKA porowatość':")
    print(weights_df.nlargest(10, 'weight_wysoka')[['dimension', 'weight_wysoka']])

    # Wizualizacja
    top_weights = weights_df.nlargest(20, 'weight_wysoka')
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_weights, x='weight_wysoka', y='dimension')
    plt.title("Top Embedding Dimensions - Wysoka Porowatość (ROC AUC 0.942)")
    plt.tight_layout()
    plt.savefig("porosity_weights.png", dpi=300)
    plt.show()

    return lr, le, auc


# Uruchom
model, label_encoder, auc_score = train_porosity_classifier()
print(f"Model gotowy! ROC AUC = {auc_score:.3f}")

# Użycie
model, label_encoder, auc_score = train_skin_type_classifier()
print(f"Model gotowy! ROC AUC = {auc_score:.3f}")

model, label_encoder, auc_score = train_hair_type_classifier()
print(f"Model gotowy! ROC AUC = {auc_score:.3f}")
