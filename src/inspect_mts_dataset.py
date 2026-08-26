from datasets import load_dataset


DATASET_NAME = "har1/MTS_Dialogue-Clinical_Note"


def main():
    dataset = load_dataset(DATASET_NAME)
    train = dataset["train"]

    print("=== DATASET OVERVIEW ===")
    print(f"Rows: {len(train)}")
    print(f"Columns: {train.column_names}")

    print("\n=== MISSING VALUES ===")
    for column in train.column_names:
        missing = sum(
            value is None or str(value).strip() == ""
            for value in train[column]
        )
        print(f"{column}: {missing}")

    print("\n=== UNIQUE VALUES ===")
    for column in train.column_names:
        print(f"{column}: {len(set(train[column]))}")

    print("\n=== EXAMPLE LENGTHS ===")
    for i in range(min(5, len(train))):
        dialogue = train[i]["dialogue"]
        summary = train[i]["section_text"]

        print(f"\nExample {i}")
        print(f"Dialogue characters: {len(dialogue)}")
        print(f"Summary characters: {len(summary)}")

    print("\n=== FIRST EXAMPLE ===")
    print(train[0])


if __name__ == "__main__":
    main()