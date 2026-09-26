# we need torch directly so we can pick a device and run inference without gradient tracking
import torch

# we need these two classes to load a real tokenizer and a real causal language model
from transformers import AutoTokenizer, AutoModelForCausalLM

# we need our shared settings so the model name and generation limits live in one place
from src.config import settings


# this function decides which hardware device to run the model on, fastest available first
def select_device() -> str:
    # a real NVIDIA GPU is fastest, so prefer it if PyTorch can see one
    if torch.cuda.is_available():
        # tell the caller to use the GPU
        return "cuda"
    # Apple Silicon's GPU backend is the next-best option on a Mac
    if torch.backends.mps.is_available():
        # tell the caller to use Apple's Metal backend
        return "mps"
    # otherwise fall back to the CPU, which always works
    return "cpu"


# this function builds the chat-format message list the tokenizer's chat template expects
def format_chat_prompt(user_message: str) -> list[dict]:
    # instruction-tuned models expect a list of role/content turns, not raw text
    return [{"role": "user", "content": user_message}]


# this function pulls a few key architecture numbers out of a model's config object
def describe_model_architecture(model_config: object) -> dict:
    # this reads how many Transformer blocks are stacked in this model
    num_layers = getattr(model_config, "num_hidden_layers", None)
    # this reads how many attention heads each block's multi-head attention uses
    num_attention_heads = getattr(model_config, "num_attention_heads", None)
    # this reads d_model, the width of every token's vector as it flows through the blocks
    hidden_size = getattr(model_config, "hidden_size", None)
    # this reads how many distinct tokens the model's vocabulary contains
    vocab_size = getattr(model_config, "vocab_size", None)
    # hand back all four numbers together so the caller can print or test them as one unit
    return {
        "num_layers": num_layers,
        "num_attention_heads": num_attention_heads,
        "hidden_size": hidden_size,
        "vocab_size": vocab_size,
    }


# this function downloads (or loads from cache) the real tokenizer and model, and prepares them for inference
def load_model_and_tokenizer(model_name: str, device: str) -> tuple:
    # this loads the tokenizer that matches the model, including its chat template
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # this downloads/loads the actual model weights
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # this moves every weight tensor onto the chosen device (cpu/mps/cuda)
    model.to(device)
    # this switches off training-only behavior like dropout, since we're only doing inference
    model.eval()
    # hand back both objects together, since they're always used as a pair
    return tokenizer, model


# this function runs one full generation: prompt in, generated reply text out
def generate_reply(tokenizer: object, model: object, device: str, prompt_messages: list[dict]) -> str:
    # this turns the chat-format messages into token IDs, adding the special tokens that cue the model to reply
    input_ids = tokenizer.apply_chat_template(prompt_messages, add_generation_prompt=True, return_tensors="pt")
    # this moves the input tensor onto the same device the model lives on
    input_ids = input_ids.to(device)
    # this disables gradient tracking, since we're not training and it would only waste memory
    with torch.no_grad():
        # this actually runs the autoregressive generation loop described in the concept doc
        output_ids = model.generate(
            input_ids,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.GENERATION_TEMPERATURE,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    # this slices off the original prompt tokens, keeping only the newly generated ones
    new_token_ids = output_ids[0][input_ids.shape[1]:]
    # this turns the generated token IDs back into readable text
    return tokenizer.decode(new_token_ids, skip_special_tokens=True)


# this is the entry point used when this script is run directly
def main() -> None:
    # this picks the fastest device available on this machine
    device = select_device()
    # this tells the user which device inference will actually run on
    print(f"using device: {device}")
    # this loads the real tokenizer and model, moved onto that device
    tokenizer, model = load_model_and_tokenizer(settings.INFERENCE_MODEL_NAME, device)
    # this is the question we'll actually ask the model, tied to our Stage 1 data
    question = "What is Home Assistant's MQTT integration used for?"
    # this builds the chat-format message list the tokenizer's template expects
    prompt_messages = format_chat_prompt(question)
    # this tokenizes the prompt so we can inspect the raw input IDs before generating anything
    input_ids = tokenizer.apply_chat_template(prompt_messages, add_generation_prompt=True, return_tensors="pt")
    # this prints the actual integer token IDs the model will see
    print(f"input token IDs: {input_ids.tolist()}")
    # this prints the shape, so you can see it's [batch_size, sequence_length]
    print(f"input shape: {tuple(input_ids.shape)}")
    # this converts the IDs back to their string pieces, so you can see the real subword split
    print(f"input tokens: {tokenizer.convert_ids_to_tokens(input_ids[0])}")
    # this pulls out the key architecture numbers for this specific real model
    architecture = describe_model_architecture(model.config)
    # this prints those numbers so you can map the concept doc's diagrams onto real values
    print(f"model architecture: {architecture}")
    # this actua`lly generates the model's reply to the question
    reply = generate_reply(tokenizer, model, device, prompt_messages)
    # this prints the final generated text
    print(f"model reply: {reply}")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off inference
    main()
