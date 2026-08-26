from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


INPUT_PATH = Path("data/processed/mts_cleaned.csv")
OUTPUT_DIR = Path("data/processed")

RANDOM_STATE = 42


def main():
    print("Loading cleaned dataset...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Total rows: {len(df)}")

    # Use dialogue as the grouping key.
    # Identical dialogues will always stay in the same split.
    groups = df["dialogue"]

    # First split:
    # 80% train
    # 20% temporary
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )

    train_indices, temp_indices = next(
        splitter.split(df, groups=groups)
    )

    train_df = df.iloc[train_indices].copy()
    temp_df = df.iloc[temp_indices].copy()

    # Second split:
    # Split the remaining 20% into:
    # 10% validation
    # 10% test
    temp_groups = temp_df["dialogue"]

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.50,
        random_state=RANDOM_STATE,
    )

    validation_indices, test_indices = next(
        splitter.split(temp_df, groups=temp_groups)
    )

    validation_df = temp_df.iloc[validation_indices].copy()
    test_df = temp_df.iloc[test_indices].copy()

    # Save files.
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_df.to_csv(
        OUTPUT_DIR / "train.csv",
        index=False,
    )

    validation_df.to_csv(
        OUTPUT_DIR / "validation.csv",
        index=False,
    )

    test_df.to_csv(
        OUTPUT_DIR / "test.csv",
        index=False,
    )

    # Print statistics.
    print("\n=== SPLIT RESULTS ===")
    print(f"Train:      {len(train_df)}")
    print(f"Validation: {len(validation_df)}")
    print(f"Test:       {len(test_df)}")
    print(f"Total:      {len(train_df) + len(validation_df) + len(test_df)}")

    # Verify that dialogues don't overlap.
    train_dialogues = set(train_df["dialogue"])
    validation_dialogues = set(validation_df["dialogue"])
    test_dialogues = set(test_df["dialogue"])

    train_validation_overlap = (
        train_dialogues & validation_dialogues
    )

    train_test_overlap = (
        train_dialogues & test_dialogues
    )

    validation_test_overlap = (
        validation_dialogues & test_dialogues
    )

    print("\n=== DATA LEAKAGE CHECK ===")
    print(
        "Train/Validation overlap:",
        len(train_validation_overlap),
    )
    print(
        "Train/Test overlap:",
        len(train_test_overlap),
    )
    print(
        "Validation/Test overlap:",
        len(validation_test_overlap),
    )

    print("\n=== FILES CREATED ===")
    print(OUTPUT_DIR / "train.csv")
    print(OUTPUT_DIR / "validation.csv")
    print(OUTPUT_DIR / "test.csv")


if __name__ == "__main__":
    main()