from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCTOR_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "doctors.csv"
)


def load_doctors():
    """Load cleaned doctor data."""

    if not DOCTOR_DATA.exists():
        raise FileNotFoundError(
            "Processed doctor dataset not found."
        )

    return pd.read_csv(DOCTOR_DATA)


def search_doctors(
    name=None,
    specialization=None,
    hospital=None,
    min_experience=None,
):
    """Search doctors using optional filters."""

    doctors = load_doctors()

    if name:
        doctors = doctors[
            doctors["name"].str.contains(
                name,
                case=False,
                na=False
            )
        ]

    if specialization:
        doctors = doctors[
            doctors["specialization"].str.contains(
                specialization,
                case=False,
                na=False
            )
        ]

    if hospital:
        doctors = doctors[
            doctors["hospital_branch"].str.contains(
                hospital,
                case=False,
                na=False
            )
        ]

    if min_experience is not None:
        doctors = doctors[
            doctors["years_experience"] >= float(min_experience)
        ]

    return doctors