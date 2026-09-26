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
