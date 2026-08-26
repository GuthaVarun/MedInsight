import pandas as pd
import re


TRAIN_PATH = "data/processed/train.csv"


def main():
    df = pd.read_csv(TRAIN_PATH)

    print("=== SUMMARY STRUCTURE ANALYSIS ===")
    print(f"Rows: {len(df)}")

    fields = {
        "Symptoms": 0,
        "Diagnosis": 0,
        "History of Patient": 0,
        "History of Complaint": 0,
        "Plan of Action": 0,
    }

    for summary in df["section_text"].fillna(""):
        for field in fields:
            if field in summary:
                fields[field] += 1

    print("\n=== FIELD FREQUENCIES ===")

    for field, count in fields.items():
        percentage = count / len(df) * 100
        print(
            f"{field}: {count} "
            f"({percentage:.2f}%)"
        )

    print("\n=== EXAMPLES OF DIFFERENT TARGETS ===")

    for i in range(min(10, len(df))):
        print("\n" + "-" * 70)
        print(f"Example {i}")
        print(df.iloc[i]["section_text"])


if __name__ == "__main__":
    main()