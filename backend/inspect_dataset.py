import os
from collections import Counter


DATASET_DIR = "dataset"


def main():

    print("=== STRUKTUR DATASET ===")

    for root, dirs, files in os.walk(DATASET_DIR):

        level = root.replace(
            DATASET_DIR,
            ""
        ).count(os.sep)

        indent = "    " * level

        print(
            f"{indent}{os.path.basename(root)}/"
        )

        subindent = "    " * (level + 1)

        for file in files[:5]:

            print(
                f"{subindent}{file}"
            )


if __name__ == "__main__":
    main()