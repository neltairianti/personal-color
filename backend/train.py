import ast
import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# =========================
# KONFIGURASI
# =========================

DATASET_FILE = "dataset_numeric.csv"
MODEL_DIR = "model"
MODEL_FILE = os.path.join(MODEL_DIR, "skin_tone_model.pkl")

FEATURE_COLUMNS = [
    "rgb_r",
    "rgb_g",
    "rgb_b",
    "lab_l",
    "lab_a",
    "lab_b",
]


# =========================
# PARSE ARRAY RGB / LAB
# =========================

def parse_array(value):
    """
    Mengubah string seperti:
    '[92.02 151.20 144.07]'
    menjadi array float.
    """

    if isinstance(value, (list, tuple, np.ndarray)):
        return np.array(value, dtype=float)

    value = str(value).strip()
    value = value.strip("[]")

    # Dataset menggunakan spasi sebagai pemisah
    values = np.fromstring(value, sep=" ")

    if len(values) != 3:
        # Coba jika ternyata menggunakan koma
        values = np.fromstring(value.replace(",", " "), sep=" ")

    if len(values) != 3:
        raise ValueError(f"Format RGB/LAB tidak valid: {value}")

    return values


# =========================
# LOAD DATASET
# =========================

print("=" * 60)
print("MEMUAT DATASET")
print("=" * 60)

df = pd.read_csv(DATASET_FILE)

print(f"Jumlah data : {len(df)}")
print(f"Kolom       : {df.columns.tolist()}")


# =========================
# PECAH RGB
# =========================

rgb_values = df["rgb"].apply(parse_array)

df["rgb_r"] = rgb_values.apply(lambda x: x[0])
df["rgb_g"] = rgb_values.apply(lambda x: x[1])
df["rgb_b"] = rgb_values.apply(lambda x: x[2])


# =========================
# PECAH LAB
# =========================

lab_values = df["lab"].apply(parse_array)

df["lab_l"] = lab_values.apply(lambda x: x[0])
df["lab_a"] = lab_values.apply(lambda x: x[1])
df["lab_b"] = lab_values.apply(lambda x: x[2])


# =========================
# CEK DATA
# =========================

print()
print("Fitur yang digunakan:")

print(df[
    [
        "label",
        "rgb_r",
        "rgb_g",
        "rgb_b",
        "lab_l",
        "lab_a",
        "lab_b",
    ]
].head())


# =========================
# SIAPKAN X DAN Y
# =========================

X = df[FEATURE_COLUMNS]
y = df["label"]


# =========================
# SPLIT DATA
# =========================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print()
print("=" * 60)
print("PEMBAGIAN DATA")
print("=" * 60)

print(f"Data training : {len(X_train)}")
print(f"Data testing  : {len(X_test)}")


# =========================
# TRAIN RANDOM FOREST
# =========================

print()
print("=" * 60)
print("TRAINING RANDOM FOREST")
print("=" * 60)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
)

model.fit(X_train, y_train)

print("Training selesai.")


# =========================
# PREDIKSI
# =========================

y_pred = model.predict(X_test)


# =========================
# EVALUASI
# =========================

accuracy = accuracy_score(y_test, y_pred)

print()
print("=" * 60)
print("HASIL EVALUASI")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")

print()
print("Classification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        digits=4,
        zero_division=0,
    )
)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# =========================
# SIMPAN MODEL
# =========================

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": FEATURE_COLUMNS,
    },
    MODEL_FILE,
)

print()
print("=" * 60)
print("MODEL DISIMPAN")
print("=" * 60)

print(f"File: {MODEL_FILE}")