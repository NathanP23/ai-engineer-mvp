# we need urllib.request from the standard library to make an HTTP GET request without adding a dependency
import urllib.request

# we need our shared settings so the repo name, branch, and output path all live in one place
from src.config import settings


# this function downloads the real CODEOWNERS file straight from home-assistant/core
def fetch_codeowners() -> str:
    # this is the raw-content URL GitHub serves plain file contents from, no API wrapper needed
    url = (
        f"https://raw.githubusercontent.com/{settings.CORE_REPO}"
        f"/{settings.CORE_REPO_BRANCH}/CODEOWNERS"
    )
    # this opens the URL and automatically closes the connection once we're done reading it
    with urllib.request.urlopen(url, timeout=settings.REQUEST_TIMEOUT_SECONDS) as response:
        # this reads the raw response bytes and decodes them as UTF-8 text
        return response.read().decode("utf-8")


# this function writes the fetched CODEOWNERS text to disk, creating the folder first if needed
def save_codeowners(codeowners_text: str) -> None:
    # this makes sure data/raw exists before we try to write a file into it
    settings.DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    # this writes the text out to the configured output path
    settings.CODEOWNERS_OUTPUT_PATH.write_text(codeowners_text)


# this is the entry point used when this script is run directly
def main() -> None:
    # this fetches the live CODEOWNERS file from GitHub
    codeowners_text = fetch_codeowners()
    # this saves it locally so later stages can read it without hitting the network again
    save_codeowners(codeowners_text)
    # this prints a friendly confirmation of what happened and where the file went
    print(f"saved CODEOWNERS ({len(codeowners_text)} bytes) to {settings.CODEOWNERS_OUTPUT_PATH}")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off the ingestion
    main()
