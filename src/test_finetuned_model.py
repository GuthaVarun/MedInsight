import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_PATH = "models/flan-t5-small-smoke-test"
TEST_PATH = "data/processed/test.csv"

NUM_EXAMPLES = 5


def generate_summary(model, tokenizer, dialogue):
    prompt = (
        "summarize clinical dialogue:\n\n"
        + dialogue
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=128,
            num_beams=4,
            early_stopping=True,
        )

    return tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True,
    )


def main():
    print("=== TESTING FINE-TUNED MODEL ===")

    df = pd.read_csv(TEST_PATH)

    print(f"Test examples available: {len(df)}")

    print("\nLoading fine-tuned model...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_PATH
    )

    model.to(torch.device("cpu"))

    print("Model loaded.")

    for i in range(min(NUM_EXAMPLES, len(df))):

        row = df.iloc[i]

        print("\n" + "=" * 80)
        print(f"EXAMPLE {i + 1}")
        print("=" * 80)

        print("\nINPUT DIALOGUE:")
        print(row["dialogue"])

        print("\nREFERENCE SUMMARY:")
        print(row["section_text"])

        summary = generate_summary(
            model,
            tokenizer,
            row["dialogue"],
        )

        print("\nFINE-TUNED MODEL SUMMARY:")
        print(summary)


if __name__ == "__main__":
    main()