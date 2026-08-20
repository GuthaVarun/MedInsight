from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "Hospitals In India (Anonymized).csv"
)

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "hospitals.csv"
)


def clean_hospitals(input_path, output_path):
    """Clean the raw hospital dataset."""

    # Load raw data
    df = pd.read_csv(input_path)

    print(f"Original records: {len(df)}")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Clean text fields
    text_columns = [
        "id",
        "city",
        "state",
        "district",
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # Convert numeric fields
    numeric_columns = [
        "density",
        "latitude",
        "longitude",
        "rating",
        "number_of_reviews",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove records missing essential information
    df = df.dropna(
        subset=[
            "id",
            "city",
            "state",
            "latitude",
            "longitude",
        ]
    )

    # Validate ratings
    df = df[
        (df["rating"] >= 0) &
        (df["rating"] <= 5)
    ]

    # Validate latitude/longitude
    df = df[
        (df["latitude"] >= -90) &
        (df["latitude"] <= 90) &
        (df["longitude"] >= -180) &
        (df["longitude"] <= 180)
    ]

    # Remove duplicate hospital IDs
    df = df.drop_duplicates(
        subset=["id"],
        keep="first"
    )

    # Sort results
    df = df.sort_values(
        by=["state", "city", "id"]
    ).reset_index(drop=True)

    # Create output directory
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save cleaned data
    df.to_csv(
        output_path,
        index=False
    )

    print(f"Cleaned records: {len(df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    clean_hospitals(
        RAW_FILE,
        PROCESSED_FILE
    )