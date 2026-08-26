from pathlib import Path

from datasets import load_dataset


DATASET_NAME = "har1/MTS_Dialogue-Clinical_Note"
OUTPUT_PATH = Path("data/processed/mts_cleaned.csv")


def clean_dialogue(text):
    """Normalize whitespace in dialogue."""
    if text is None:
        return ""

    return " ".join(str(text).split())


def clean_summary(text):
    """Normalize summary while preserving section boundaries."""
    if text is None:
        return ""

    lines = []

    for line in str(text).splitlines():
        line = " ".join(line.split())

        if line:
            lines.append(line)

    return "\n".join(lines)


def main():
    dataset = load_dataset(DATASET_NAME)
    data = dataset["train"]

    print("=== ORIGINAL DATASET ===")
    print(f"Original rows: {len(data)}")

    # Keep only the fields needed for summarization.
    data = data.select_columns(
        ["ID", "section_header", "dialogue", "section_text"]
    )

    # Remove missing/empty dialogue or summary.
    data = data.filter(
        lambda row: (
            row["dialogue"] is not None
            and row["section_text"] is not None
            and row["dialogue"].strip() != ""
            and row["section_text"].strip() != ""
        )
    )

    # Clean the input and target separately.
    data = data.map(
        lambda row: {
            "dialogue": clean_dialogue(row["dialogue"]),
            "section_text": clean_summary(row["section_text"]),
        }
    )

    data = data.to_pandas()

    # Analyze duplicate dialogues.
    duplicate_dialogues = data[
        data.duplicated(subset=["dialogue"], keep=False)
    ]

    print("\n=== DUPLICATE ANALYSIS ===")
    print(
        f"Rows involved in duplicate dialogues: "
        f"{len(duplicate_dialogues)}"
    )

    conflicting_duplicates = (
        duplicate_dialogues
        .groupby("dialogue")["section_text"]
        .nunique()
    )

    conflicting_duplicates = conflicting_duplicates[
        conflicting_duplicates > 1
    ]

    print(
        f"Duplicate dialogues with different summaries: "
        f"{len(conflicting_duplicates)}"
    )

    # Remove only exact duplicate records.
    before = len(data)

    data = data.drop_duplicates(
        subset=[
            "section_header",
            "dialogue",
            "section_text",
        ]
    )

    removed = before - len(data)

    print("\n=== EXACT DUPLICATE REMOVAL ===")
    print(f"Exact duplicate rows removed: {removed}")

    print("\n=== FINAL RESULT ===")
    print(f"Rows after cleaning: {len(data)}")

    # Create output directory if necessary.
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save cleaned dataset.
    data.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\n=== SAVED DATASET ===")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Rows saved: {len(data)}")


if __name__ == "__main__":
    main()