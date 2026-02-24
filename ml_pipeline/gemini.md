# Gemini CLI: ML Pipeline & Fine-Tuning Context

## Purpose
Fine-tune and export Llama-3-8B for binary classification.

## Tasks
- **Fine-Tuning:** Unsloth + QLoRA notebook (`finetune_llama3_8b.ipynb`).
- **Target:** 2-class classification ("SAFE" or "FLAGGED").
- **Quantization:** Export LoRA adapters/base model to GGUF format for `llama.cpp`.
- **Validation:** Ensure the GGUF model returns deterministic outputs (SAFE/FLAGGED) with < 50ms latency per inference.

## Key Files
- `finetune_llama3_8b.ipynb`: Jupyter notebook for training.
- `export_gguf.md`: Documentation and scripts for GGUF conversion.
- `requirements.txt`: Training dependencies (`unsloth`, `torch`, `peft`, `bitsandbytes`, etc.).

## Hyperparameters (Draft)
- **Batch Size:** 4
- **Gradient Accumulation:** 4
- **Epochs:** 1-3
- **Learning Rate:** 2e-4
- **LoRA Rank (r):** 16-32
- **Alpha:** 32-64
