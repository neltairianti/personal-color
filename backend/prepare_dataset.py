import os
import cv2
import pandas as pd

from color_utils import extract_features


DATASET_DIR = "dataset"
OUTPUT_FILE = "dataset_numeric.csv"

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


def main():

    rows = []

    print("===================================")
    print(" KONVERSI DATASET GAMBAR → NUMERIK")
    print("===================================")

    for root, dirs, files in os.walk(DATASET_DIR):

        for filename in files:

            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue

            image_path = os.path.join(root, filename)

            print(f"Memproses: {image_path}")

            image = cv2.imread(image_path)

            if image is None:
                print("  [SKIP] Gambar tidak dapat dibaca")
                continue

            try:

                features = extract_features(image)

                # Label diasumsikan berasal dari nama folder
                label = os.path.basename(root)

                row = {
                    "filename": filename,
                    "label": label,
                    **features
                }

                rows.append(row)

                print("  [OK]")

            except Exception as e:

                print(f"  [SKIP] {e}")

    if not rows:
        print("\nTidak ada data yang berhasil diproses.")
        return

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n===================================")
    print(" SELESAI")
    print("===================================")

    print(f"Jumlah data : {len(df)}")
    print(f"File        : {OUTPUT_FILE}")

    print("\nContoh data:")
    print(df.head())


if __name__ == "__main__":
    main()