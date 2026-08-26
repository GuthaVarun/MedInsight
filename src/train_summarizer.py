from pathlib import Path

import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)


MODEL_NAME = "google/flan-t5-small"

TRAIN_PATH = "data/processed/train.csv"
VALIDATION_PATH = "data/processed/validation.csv"

OUTPUT_DIR = Path("models/flan-t5-small-smoke-test")

MAX_INPUT_LENGTH = 512
MAX_TARGET_LENGTH = 128

# Smoke-test settings
SMOKE_TEST = False
SMOKE_TEST_SIZE = 50


def load_data(path):
    df = pd.read_csv(path)

    # Keep only the columns needed by the model.
    df = df[["dialogue", "section_text"]]

    return Dataset.from_pandas(
        df,
        preserve_index=False,
    )


def preprocess_function(examples, tokenizer):
    prompts = [
        "summarize clinical dialogue:\n\n" + dialogue
        for dialogue in examples["dialogue"]
    ]

    model_inputs = tokenizer(
        prompts,
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    )

    labels = tokenizer(
        text_target=examples["section_text"],
        max_length=MAX_TARGET_LENGTH,
        truncation=True,
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs


def main():
    print("=== MEDINSIGHTS SUMMARIZER TRAINING ===")

    if SMOKE_TEST:
        print("MODE: SMOKE TEST")
        print(f"Training examples: {SMOKE_TEST_SIZE}")
    else:
        print("MODE: FULL TRAINING")

    print(f"Model: {MODEL_NAME}")
    print(f"Input max length: {MAX_INPUT_LENGTH}")
    print(f"Target max length: {MAX_TARGET_LENGTH}")

    # ---------------------------------------------------------
    # Load tokenizer and model
    # ---------------------------------------------------------

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    print("Loading model...")

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    print("Model loaded.")

    # ---------------------------------------------------------
    # Load datasets
    # ---------------------------------------------------------

    print("\nLoading training dataset...")

    train_dataset = load_data(TRAIN_PATH)

    print(f"Training examples available: {len(train_dataset)}")

    print("Loading validation dataset...")

    validation_dataset = load_data(VALIDATION_PATH)

    print(
        f"Validation examples available: "
        f"{len(validation_dataset)}"
    )

    # Use only a small subset for the smoke test.
    if SMOKE_TEST:
        train_dataset = train_dataset.select(
            range(
                min(
                    SMOKE_TEST_SIZE,
                    len(train_dataset),
                )
            )
        )

    print(
        f"\nTraining examples used: "
        f"{len(train_dataset)}"
    )

    # ---------------------------------------------------------
    # Tokenization
    # ---------------------------------------------------------

    print("\nTokenizing training data...")

    train_dataset = train_dataset.map(
        lambda examples: preprocess_function(
            examples,
            tokenizer,
        ),
        batched=True,
        remove_columns=train_dataset.column_names,
    )

    print("Tokenizing validation data...")

    validation_dataset = validation_dataset.map(
        lambda examples: preprocess_function(
            examples,
            tokenizer,
        ),
        batched=True,
        remove_columns=validation_dataset.column_names,
    )

    print("Tokenization complete.")

    # ---------------------------------------------------------
    # Data collator
    # ---------------------------------------------------------

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
    )

    # ---------------------------------------------------------
    # Training configuration
    # ---------------------------------------------------------

    training_args = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR),

        # Smoke test
        num_train_epochs=1,

        # CPU-friendly
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,

        # Accumulate gradients instead of using large batches.
        gradient_accumulation_steps=2,

        learning_rate=5e-5,

        # Evaluate once after the epoch.
        eval_strategy="epoch",

        save_strategy="epoch",

        logging_strategy="steps",
        logging_steps=5,

        # Keep only the best/latest checkpoint.
        save_total_limit=1,

        # CPU
        use_cpu=True,

        # No mixed precision on CPU.
        fp16=False,
        bf16=False,

        report_to="none",

        # Don't remove columns needed by the data collator.
        remove_unused_columns=False,
    )

    # ---------------------------------------------------------
    # Trainer
    # ---------------------------------------------------------

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    # ---------------------------------------------------------
    # Train
    # ---------------------------------------------------------

    print("\n=== STARTING TRAINING ===")

    trainer.train()

    # ---------------------------------------------------------
    # Save model
    # ---------------------------------------------------------

    print("\n=== SAVING MODEL ===")

    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))

    print(f"Model saved to: {OUTPUT_DIR}")

    print("\n=== SMOKE TEST COMPLETE ===")


if __name__ == "__main__":
    main()