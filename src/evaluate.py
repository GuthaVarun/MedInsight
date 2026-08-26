import re
from pathlib import Path

import pandas as pd
import torch
import evaluate as hf_evaluate
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_PATH = "models/flan-t5-small-smoke-test"
TEST_PATH = "data/processed/test.csv"

MAX_INPUT_LENGTH = 512
MAX_NEW_TOKENS = 128
NUM_BEAMS = 4


# =========================================================
# GENERATE SUMMARY
# =========================================================

def generate_summary(model, tokenizer, dialogue):
    """
    Generate a clinical summary from a doctor-patient dialogue.
    """

    prompt = (
        "summarize clinical dialogue:\n\n"
        + dialogue
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_LENGTH,
    )

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=NUM_BEAMS,
            early_stopping=True,
        )

    summary = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True,
    )

    return summary


# =========================================================
# COUNT N/A FIELDS
# =========================================================

def count_na_fields(summary):
    """
    Count how many clinical fields were generated as N/A.
    """

    fields = [
        "Symptoms:",
        "Diagnosis:",
        "History of Patient:",
        "History of Complaint:",
        "Plan of Action:",
    ]

    na_count = 0

    for field in fields:

        pattern = (
            rf"{re.escape(field)}\s*N/?A\.?"
        )

        if re.search(
            pattern,
            summary,
            re.IGNORECASE,
        ):
            na_count += 1

    return na_count


# =========================================================
# MAIN
# =========================================================

def main():

    print("=== MEDINSIGHTS MODEL EVALUATION ===")

    # -----------------------------------------------------
    # Load test dataset
    # -----------------------------------------------------

    df = pd.read_csv(TEST_PATH)

    print(
        f"Test examples: {len(df)}"
    )

    # -----------------------------------------------------
    # Load tokenizer and model
    # -----------------------------------------------------

    print(
        "\nLoading fine-tuned model..."
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_PATH
    )

    device = torch.device("cpu")

    model.to(device)
    model.eval()

    print("Model loaded.")
    print(f"Device: {device}")

    # -----------------------------------------------------
    # Generate predictions
    # -----------------------------------------------------

    predictions = []
    references = []

    na_field_counts = []
    prediction_lengths = []

    print(
        "\nGenerating predictions..."
    )

    for i, row in df.iterrows():

        prediction = generate_summary(
            model,
            tokenizer,
            row["dialogue"],
        )

        reference = row["section_text"]

        predictions.append(
            prediction
        )

        references.append(
            reference
        )

        na_field_counts.append(
            count_na_fields(prediction)
        )

        prediction_lengths.append(
            len(prediction.split())
        )

        if (i + 1) % 10 == 0:

            print(
                f"Processed "
                f"{i + 1}/{len(df)}"
            )

    # -----------------------------------------------------
    # SAVE PREDICTIONS FIRST
    # -----------------------------------------------------

    output_dir = Path(
        "data/processed"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = pd.DataFrame(
        {
            "dialogue": df["dialogue"],
            "reference": references,
            "prediction": predictions,
            "na_fields": na_field_counts,
        }
    )

    output_path = (
        output_dir
        / "model_predictions.csv"
    )

    results.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nPredictions saved to: "
        f"{output_path}"
    )

    # -----------------------------------------------------
    # ROUGE
    # -----------------------------------------------------

    print(
        "\nLoading ROUGE evaluator..."
    )

    try:

        rouge = hf_evaluate.load(
            "rouge"
        )

        rouge_scores = rouge.compute(
            predictions=predictions,
            references=references,
        )

        print(
            "\n=== ROUGE SCORES ==="
        )

        for metric, score in rouge_scores.items():

            print(
                f"{metric}: "
                f"{score:.4f}"
            )

    except Exception as error:

        print(
            "\nROUGE evaluation failed."
        )

        print(
            f"Error: {error}"
        )

        print(
            "\nThe predictions have already "
            "been saved, so they are not lost."
        )

    # -----------------------------------------------------
    # N/A ANALYSIS
    # -----------------------------------------------------

    print(
        "\n=== N/A ANALYSIS ==="
    )

    total_na = sum(
        na_field_counts
    )

    average_na = (
        total_na
        / len(predictions)
    )

    print(
        f"Total N/A fields generated: "
        f"{total_na}"
    )

    print(
        f"Average N/A fields per summary: "
        f"{average_na:.2f}"
    )

    collapsed_outputs = sum(
        count >= 3
        for count in na_field_counts
    )

    print(
        f"Outputs with 3+ N/A fields: "
        f"{collapsed_outputs}/"
        f"{len(predictions)}"
    )

    # -----------------------------------------------------
    # SUMMARY LENGTH
    # -----------------------------------------------------

    print(
        "\n=== SUMMARY LENGTH ==="
    )

    average_length = (
        sum(prediction_lengths)
        / len(prediction_lengths)
    )

    print(
        f"Average generated words: "
        f"{average_length:.2f}"
    )

    # -----------------------------------------------------
    # SAMPLE RESULTS
    # -----------------------------------------------------

    print(
        "\n=== SAMPLE RESULTS ==="
    )

    for i in range(
        min(5, len(df))
    ):

        print(
            "\n"
            + "=" * 70
        )

        print(
            f"EXAMPLE {i + 1}"
        )

        print(
            "=" * 70
        )

        print(
            "\nREFERENCE:"
        )

        print(
            references[i]
        )

        print(
            "\nPREDICTION:"
        )

        print(
            predictions[i]
        )

    # -----------------------------------------------------
    # COMPLETE
    # -----------------------------------------------------

    print(
        "\n=== EVALUATION COMPLETE ==="
    )

    print(
        f"Prediction file: "
        f"{output_path}"
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()