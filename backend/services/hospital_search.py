from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

HOSPITAL_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "hospitals.csv"
)


def load_hospitals():
    """Load cleaned hospital data."""

    if not HOSPITAL_DATA.exists():
        raise FileNotFoundError(
            "Processed hospital dataset not found."
        )

    return pd.read_csv(HOSPITAL_DATA)


def search_hospitals(
    city=None,
    state=None,
    min_rating=None,
):
    """Search hospitals using optional filters."""

    hospitals = load_hospitals()

    if city:
        hospitals = hospitals[
            hospitals["city"]
            .str.contains(
                city,
                case=False,
                na=False
            )
        ]

    if state:
        hospitals = hospitals[
            hospitals["state"]
            .str.contains(
                state,
                case=False,
                na=False
            )
        ]

    if min_rating is not None:
        hospitals = hospitals[
            hospitals["rating"] >= float(min_rating)
        ]

    return hospitals