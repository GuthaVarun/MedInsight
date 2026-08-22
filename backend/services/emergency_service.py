from backend.services.hospital_search import search_hospitals


def find_emergency_hospitals(
    city=None,
    state=None,
    min_rating=None,
):
    hospitals = search_hospitals(
        city=city,
        state=state,
        min_rating=min_rating,
    )

    if "rating" in hospitals.columns:
        hospitals = hospitals.sort_values(
            by=["rating", "number_of_reviews"],
            ascending=[False, False],
        )

    return hospitals