from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import os

# Configuration
MODEL_NAME = "unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit"
DATASET_PATH = "data_generator/dataset.jsonl"
OUTPUT_DIR = "ml_pipeline/qwen_schema_guardian"

def main():
    # 1. Load Model (Optimized for 4GB VRAM)
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_NAME,
        max_seq_length = 1024,
        load_in_4bit = True,
    )

    # 2. Add LoRA Adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r = 8,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
    )

    # 3. Format Data
    def formatting_prompts_func(examples):
        instructions = ["Classify the following financial message as 'SAFE' or 'FLAGGED' based on semantic integrity."] * len(examples["message"])
        inputs       = [str(m) for m in examples["message"]]
        outputs      = examples["label"]
        texts = []
        for instruction, input, output in zip(instructions, inputs, outputs):
            # Qwen-style ChatML format using triple quotes for multi-line stability
            text = f"""<|im_start|>system
            {instruction}<|im_end|>
            <|im_start|>user
            {input}<|im_end|>
            <|im_start|>assistant
            {output}<|im_end|>"""
            texts.append(text)
        return { "text" : texts }

    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
    dataset = dataset.map(formatting_prompts_func, batched = True)

    # 4. Trainer Configuration
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = 1024,
        dataset_num_proc = 2,
        args = TrainingArguments(
            per_device_train_batch_size = 1,
            gradient_accumulation_steps = 8,
            warmup_steps = 5,
            max_steps = 100, # Initial quick run; increase for full training
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 10,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = OUTPUT_DIR,
        ),
    )

    # 5. Execute Training
    print("Starting fine-tuning...")
    trainer.train()

    # 6. Save GGUF (Optimized for Inference Sidecar)
    print("Exporting to GGUF...")
    model.save_pretrained_gguf(OUTPUT_DIR, tokenizer, quantization_method = "q4_k_m")
    print(f"Success! Model saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
