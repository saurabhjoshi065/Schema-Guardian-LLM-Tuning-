# Exporting to GGUF for llama.cpp

This guide provides the steps to export the fine-tuned Llama-3-8B model for consumption by the inference sidecar.

## Prerequisites
- Fine-tuned adapter from `finetune_llama3_8b.ipynb`.
- Unsloth or `llama.cpp`'s `convert.py` script.

## Method A: Unsloth Export (Recommended)
Unsloth provides a built-in method for GGUF export.
```python
from unsloth import FastLanguageModel

# Save to 4-bit GGUF (High efficiency)
model.save_pretrained_gguf("llama-3-8b-schema-guardian", tokenizer, quantization_method = "q4_k_m")
```

## Method B: llama.cpp Manual Export
1.  **Clone llama.cpp:**
    ```bash
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    ```
2.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Merge & Convert:**
    Assuming your model is in HF format:
    ```bash
    python convert.py /path/to/fine-tuned-hf --outfile llama-3-8b-schema-guardian.gguf --outtype q4_k_m
    ```

## Validation
After export, verify the GGUF model can load and return deterministic outputs.
1.  **Load check:**
    ```bash
    ./main -m llama-3-8b-schema-guardian.gguf -n 1 --prompt "Classify: {'amount': 100}"
    ```
2.  **Output Check:** Ensure it returns only "SAFE" or "FLAGGED" without hallucinations.

## Deployment
Move the resulting `.gguf` file to:
- `inference_sidecar/models/llama-3-8b-schema-guardian.gguf`
