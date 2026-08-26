import pandas as pd
from transformers import AutoTokenizer


MODEL_NAME = "google/flan-t5-small"

TRAIN_PATH = "data/processed/train.csv"
VALIDATION_PATH = "data/processed/validation.csv"
TEST_PATH = "data/processed/test.csv"

MAX_INPUT_LENGTH = 512
MAX_TARGET_LENGTH = 128


def analyze_file(tokenizer, path):
    df = pd.read_csv(path)

    input_lengths = []
    target_lengths = []

    input_over_limit = 0
    target_over_limit = 0

    for _, row in df.iterrows():

        input_tokens = tokenizer(
            f"summarize clinical dialogue:\n\n{row['dialogue']}",
            truncation=False,
        )["input_ids"]

        target_tokens = tokenizer(
            row["section_text"],
            truncation=False,
        )["input_ids"]

        input_length = len(input_tokens)
        target_length = len(target_tokens)

        input_lengths.append(input_length)
        target_lengths.append(target_length)

        if input_length > MAX_INPUT_LENGTH:
            input_over_limit += 1

        if target_length > MAX_TARGET_LENGTH:
            target_over_limit += 1

    print(f"\n=== {path} ===")
    print(f"Rows: {len(df)}")

    print("\nInput token lengths:")
    print(f"Min:    {min(input_lengths)}")
    print(f"Max:    {max(input_lengths)}")
    print(f"Mean:   {sum(input_lengths) / len(input_lengths):.1f}")

    print(f"\nInputs > {MAX_INPUT_LENGTH} tokens:")
    print(f"Count: {input_over_limit}")
    print(
        f"Percentage: "
        f"{input_over_limit / len(df) * 100:.2f}%"
    )

    print("\nTarget token lengths:")
    print(f"Min:    {min(target_lengths)}")
    print(f"Max:    {max(target_lengths)}")
    print(f"Mean:   {sum(target_lengths) / len(target_lengths):.1f}")

    print(f"\nTargets > {MAX_TARGET_LENGTH} tokens:")
    print(f"Count: {target_over_limit}")
    print(
        f"Percentage: "
        f"{target_over_limit / len(df) * 100:.2f}%"
    )


def main():
    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Tokenizer loaded.")

    analyze_file(tokenizer, TRAIN_PATH)
    analyze_file(tokenizer, VALIDATION_PATH)
    analyze_file(tokenizer, TEST_PATH)


if __name__ == "__main__":
    main()