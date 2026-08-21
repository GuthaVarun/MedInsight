from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "doctors.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DATA = PROCESSED_DIR / "doctors.csv"


def clean_doctors():
    """Load, clean, validate, and save doctor data."""

    if not RAW_DATA.exists():
        raise FileNotFoundError(
            f"Doctor dataset not found: {RAW_DATA}"
        )

    df = pd.read_csv(RAW_DATA)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate doctor records
    df = df.drop_duplicates(subset=["doctor_id"])

    # Clean text fields
    text_columns = [
        "doctor_id",
        "first_name",
        "last_name",
        "specialization",
        "phone_number",
        "hospital_branch",
        "email",
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # Create a full name for searching
    df["name"] = (
        df["first_name"] + " " + df["last_name"]
    ).str.strip()

    # Ensure experience is numeric
    df["years_experience"] = pd.to_numeric(
        df["years_experience"],
        errors="coerce"
    )

    # Remove records with invalid experience
    df = df.dropna(subset=["years_experience"])

    # Experience cannot be negative
    df = df[df["years_experience"] >= 0]

    # Convert experience to integer
    df["years_experience"] = df["years_experience"].astype(int)

    # Save cleaned dataset
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_DATA, index=False)

    print(f"Cleaned {len(df)} doctor records.")
    print(f"Saved to: {PROCESSED_DATA}")


if __name__ == "__main__":
    clean_doctors()