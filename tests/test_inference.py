# we need SimpleNamespace to build a fake model-config object without loading a real model
from types import SimpleNamespace

# we need the inference module to test its pure, network-free functions
from src.inference import generate


# this test checks that format_chat_prompt wraps a plain string into the expected chat-role shape
def test_format_chat_prompt_builds_single_user_turn() -> None:
    # this calls the function under test with a plain question
    prompt_messages = generate.format_chat_prompt("What is MQTT?")
    # this checks the output is a one-turn list with the "user" role and the original text
    assert prompt_messages == [{"role": "user", "content": "What is MQTT?"}]


# this test checks that describe_model_architecture reads the four expected fields off a config object
def test_describe_model_architecture_extracts_expected_fields() -> None:
    # this is a fake config shaped like a real Hugging Face model config, without loading any model
    fake_config = SimpleNamespace(
        num_hidden_layers=30,
        num_attention_heads=9,
        hidden_size=576,
        vocab_size=49152,
    )
    # this calls the function under test
    architecture = generate.describe_model_architecture(fake_config)
    # this checks every field was read out correctly
    assert architecture == {
        "num_layers": 30,
        "num_attention_heads": 9,
        "hidden_size": 576,
        "vocab_size": 49152,
    }


# this test checks that a config object missing a field doesn't crash, it just reports None for it
def test_describe_model_architecture_handles_missing_field() -> None:
    # this fake config is missing "vocab_size" entirely, unlike a real config
    fake_config = SimpleNamespace(num_hidden_layers=12, num_attention_heads=8, hidden_size=768)
    # this calls the function under test
    architecture = generate.describe_model_architecture(fake_config)
    # this checks the missing field was safely defaulted to None instead of raising an error
    assert architecture["vocab_size"] is None
