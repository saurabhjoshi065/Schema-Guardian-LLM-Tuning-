import os
import time
import psutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI(title="Schema-Guardian Inference Sidecar")

# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "models/qwen2.5-1.5b-schema-guardian.gguf")
CONTEXT_SIZE = 1024

# Global Model Variable
llm = None

class ValidationRequest(BaseModel):
    message: dict

class ValidationResponse(BaseModel):
    label: str  # "SAFE" or "FLAGGED"
    latency_ms: float

@app.on_event("startup")
def load_model():
    global llm
    print(f"Loading model from {MODEL_PATH}...")
    if not os.path.exists(MODEL_PATH):
        print(f"Warning: Model file not found at {MODEL_PATH}. Inference will fail until a model is provided.")
        return
    
    # Initialize Qwen2.5-1.5B with GGUF
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=CONTEXT_SIZE,
        n_threads=psutil.cpu_count(logical=False),
        verbose=False
    )
    
    # Warmup
    print("Warming up model...")
    warmup_prompt = "<|im_start|>system\nClassify as SAFE or FLAGGED.<|im_end|>\n<|im_start|>user\n{'amount': 100}<|im_end|>\n<|im_start|>assistant\n"
    llm(warmup_prompt, max_tokens=1)
    print("Model ready.")

@app.post("/validate", response_model=ValidationResponse)
async def validate_message(request: ValidationRequest):
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Check server logs.")

    start_time = time.time()
    
    # Qwen-style Prompt Template
    prompt = f"""<|im_start|>system
Classify the following financial message as 'SAFE' or 'FLAGGED' based on semantic integrity.
<|im_end|>
<|im_start|>user
{request.message}
<|im_end|>
<|im_start|>assistant
"""
    
    try:
        output = llm(
            prompt,
            max_tokens=1,
            stop=["\n"],
            echo=False,
            temperature=0.0 # Deterministic
        )
        
        prediction = output["choices"][0]["text"].strip().upper()
        
        # Mapping to expected labels
        label = "SAFE" if "SAFE" in prediction else "FLAGGED"
        
        latency = (time.time() - start_time) * 1000
        return ValidationResponse(label=label, latency_ms=latency)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": llm is not None}
