# model.py
# Loads Qwen 2.5 from HuggingFace Hub
# Runs on AMD MI300X via ROCm

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print(f"[~] Loading {MODEL_NAME} from HuggingFace Hub...")
print(f"[*] AMD ROCm Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",       # AMD MI300X via ROCm
    trust_remote_code=True
)

model.eval()
print(f"[+] Model loaded on: {next(model.parameters()).device}")


def chat(system_prompt: str, user_input: str, max_new_tokens: int = 512) -> str:
    """
    Single function to call Qwen from anywhere in the codebase.
    Drop-in replacement for ollama.chat()
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Strip the input tokens — return only new tokens
    generated = output_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()
