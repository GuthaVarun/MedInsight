import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-small"
TEST_PATH = "data/processed/test.csv"


def main():
    print("Loading test dataset...")

    df = pd.read_csv(TEST_PATH)

    print(f"Test examples: {len(df)}")

    # Take one real example from our test set.
    dialogue = df.iloc[0]["dialogue"]
    reference = df.iloc[0]["section_text"]

    print("\n=== INPUT DIALOGUE ===")
    print(dialogue)

    print("\n=== REFERENCE SUMMARY ===")
    print(reference)

    print("\n=== LOADING MODEL ===")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    device = torch.device("cpu")
    model.to(device)

    print("Model loaded successfully.")
    print(f"Device: {device}")

    # Give FLAN-T5 an explicit summarization instruction.
    prompt = (
        "Summarize the following doctor-patient clinical dialogue "
        "into a concise clinical note:\n\n"
        f"{dialogue}"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    print("\n=== GENERATING SUMMARY ===")

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            num_beams=2,
        )

    print("\n=== RAW OUTPUT IDS ===")
    print(output_ids)

    print("\n=== RAW OUTPUT LENGTH ===")
    print(output_ids.shape)

    generated_summary = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=False,
    )

    print("\n=== MODEL SUMMARY INCLUDING SPECIAL TOKENS ===")
    print(repr(generated_summary))


if __name__ == "__main__":
    main()