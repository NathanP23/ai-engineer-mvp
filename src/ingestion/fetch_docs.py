# we need urllib.request from the standard library to make an HTTP GET request without adding a dependency
import urllib.request

# we need our shared settings so repo names, branch, the slug list, and output paths all live in one place
from src.config import settings


# this function builds the raw-content URL for one integration's real documentation page
def build_doc_url(integration_slug: str) -> str:
    # this points at the exact file path Home Assistant's docs site uses for each integration
    return (
        f"https://raw.githubusercontent.com/{settings.DOCS_REPO}"
        f"/{settings.DOCS_REPO_BRANCH}/source/_integrations/{integration_slug}.markdown"
    )


# this function downloads one integration's real documentation page as plain markdown text
def fetch_doc(integration_slug: str) -> str:
    # this builds the URL for the specific integration we were asked to fetch
    url = build_doc_url(integration_slug)
    # this opens the URL and automatically closes the connection once we're done reading it
    with urllib.request.urlopen(url, timeout=settings.REQUEST_TIMEOUT_SECONDS) as response:
        # this reads the raw response bytes and decodes them as UTF-8 markdown text
        return response.read().decode("utf-8")


# this function saves one fetched doc page to its own file under data/raw/docs
def save_doc(integration_slug: str, markdown_text: str) -> None:
    # this makes sure the docs output folder exists before we try to write into it
    settings.DOCS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # this builds the exact file path this integration's doc should be saved to
    output_path = settings.DOCS_OUTPUT_DIR / f"{integration_slug}.md"
    # this writes the markdown text out to that path
    output_path.write_text(markdown_text)


# this is the entry point used when this script is run directly
def main() -> None:
    # this walks through every integration slug in our fixed, tiny sample list
    for integration_slug in settings.SAMPLE_INTEGRATION_SLUGS:
        # this downloads the real doc page for the current integration
        markdown_text = fetch_doc(integration_slug)
        # this saves it locally so later stages can chunk and embed it without hitting the network again
        save_doc(integration_slug, markdown_text)
        # this prints a friendly, per-file confirmation as ingestion progresses
        print(f"saved doc for '{integration_slug}' ({len(markdown_text)} bytes)")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off the ingestion
    main()
