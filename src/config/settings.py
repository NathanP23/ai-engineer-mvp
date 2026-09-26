# we need Path so we can build filesystem-safe, cross-platform output paths
from pathlib import Path

# this is the real GitHub repo that holds Home Assistant's source code, issues, and CODEOWNERS
CORE_REPO = "home-assistant/core"

# this is the branch of the core repo where CODEOWNERS actually lives
CORE_REPO_BRANCH = "dev"

# this is the real GitHub repo that holds Home Assistant's public documentation site
DOCS_REPO = "home-assistant/home-assistant.io"

# this is the branch of the docs repo where the integration markdown pages live
DOCS_REPO_BRANCH = "current"

# this is a small, fixed, representative sample of integrations, chosen once so ingestion is reproducible and the corpus stays tiny
SAMPLE_INTEGRATION_SLUGS = [
    "mqtt",
    "zwave_js",
    "hue",
    "sonos",
    "unifi",
    "nest",
    "ring",
    "tesla_fleet",
    "plex",
    "spotify",
    "google",
    "alexa",
    "template",
    "rest",
    "sql",
]

# this is how many items we ask GitHub for per page (its max is 100); many of these are pull
# requests we filter out afterward, so the real number of saved issues ends up smaller than this
ISSUE_SAMPLE_SIZE = 100

# this is the root folder where every raw, unprocessed ingested file gets written
DATA_RAW_DIR = Path("data/raw")

# this is the subfolder where fetched documentation markdown files are saved
DOCS_OUTPUT_DIR = DATA_RAW_DIR / "docs"

# this is the single JSON file where fetched GitHub issues are saved
ISSUES_OUTPUT_PATH = DATA_RAW_DIR / "issues.json"

# this is the single text file where the fetched CODEOWNERS content is saved
CODEOWNERS_OUTPUT_PATH = DATA_RAW_DIR / "codeowners.txt"

# this is how many seconds we wait for any single network call before giving up
REQUEST_TIMEOUT_SECONDS = 15

# this is the small, real, instruction-tuned open-source model used for direct HF/PyTorch inference
INFERENCE_MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"

# this caps how many new tokens the model is allowed to generate per reply, so a run can't run forever
MAX_NEW_TOKENS = 80

# this controls how random generation is: 0.0 is fully deterministic, higher values are more varied
GENERATION_TEMPERATURE = 0.7

# this is the root folder where every derived (chunked/embedded) file gets written, kept separate
# from data/raw so raw source data is never mixed with things we can regenerate from it
DATA_PROCESSED_DIR = Path("data/processed")

# this is the single JSON file where chunked (but not yet embedded) documents are saved
CHUNKS_OUTPUT_PATH = DATA_PROCESSED_DIR / "chunks.json"

# this is the single JSON file where chunks plus their embedding vectors are saved
EMBEDDED_CHUNKS_OUTPUT_PATH = DATA_PROCESSED_DIR / "embedded_chunks.json"

# this is how many characters each chunk contains, small enough to fit comfortably in an LLM's context window
CHUNK_SIZE_CHARS = 800

# this is how many characters consecutive chunks share, so a sentence split across a chunk boundary isn't lost
CHUNK_OVERLAP_CHARS = 150

# this is the small, real embedding model used to turn each chunk of text into a similarity-searchable vector
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

