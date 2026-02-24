# Gemini CLI: ML Pipeline & Fine-Tuning Context

## Purpose
Fine-tune and export **Qwen2.5-1.5B** for binary classification (optimized for 4GB VRAM).

## Tasks
- **Fine-Tuning:** Unsloth + QLoRA notebook (`finetune_qwen_1_5b.ipynb`).
- **Low-VRAM Script:** Standalone training script (`train_low_vram.py`).
- **Target:** 2-class classification ("SAFE" or "FLAGGED").
- **Quantization:** Export to GGUF format for `llama.cpp`.

## Hyperparameters (Optimized for GTX 1650)
- **Model:** `unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit`
- **Batch Size:** 1-2
- **Gradient Accumulation:** 8
- **LoRA Rank (r):** 8
- **Alpha:** 16
