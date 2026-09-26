# we need json to parse GitHub's API response and to write our simplified issues back out
import json

# we need urllib.request from the standard library to make an HTTP GET request without adding a dependency
import urllib.request

# we need urllib.parse to safely build the query string for the GitHub API call
import urllib.parse

# we need our shared settings so the repo name, sample size, and output path all live in one place
from src.config import settings


# this function calls the real GitHub Issues API and returns real, raw issues (with pull requests filtered out)
def fetch_issues() -> list[dict]:
    # this is the GitHub REST endpoint that lists issues for a single repository
    base_url = f"https://api.github.com/repos/{settings.CORE_REPO}/issues"
    # this builds the query string asking for both open and closed issues, capped at our sample size
    query_string = urllib.parse.urlencode({"state": "all", "per_page": settings.ISSUE_SAMPLE_SIZE})
    # this combines the base URL and query string into the final request URL
    url = f"{base_url}?{query_string}"
    # this builds the request with a User-Agent header, which GitHub's API requires from callers
    request = urllib.request.Request(url, headers={"User-Agent": "ai-engineer-mvp-ingestion"})
    # this opens the URL and automatically closes the connection once we're done reading it
    with urllib.request.urlopen(request, timeout=settings.REQUEST_TIMEOUT_SECONDS) as response:
        # this reads and decodes the response body, then parses it as JSON
        all_items = json.loads(response.read().decode("utf-8"))
    # GitHub's issues endpoint also returns pull requests mixed in, and we only want real tickets
    return [item for item in all_items if "pull_request" not in item]


# this function strips one raw GitHub issue down to just the fields our future MCP server will actually use
def simplify_issue(raw_issue: dict) -> dict:
    # this keeps only the fields we care about, so downstream code isn't coupled to GitHub's full schema
    return {
        "id": raw_issue["number"],
        "title": raw_issue["title"],
        "body": raw_issue.get("body") or "",
        "state": raw_issue["state"],
        "url": raw_issue["html_url"],
    }


# this function writes the simplified issue list to disk as a single JSON file
def save_issues(issues: list[dict]) -> None:
    # this makes sure data/raw exists before we try to write a file into it
    settings.DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    # this writes the issues out as nicely indented, human-readable JSON
    settings.ISSUES_OUTPUT_PATH.write_text(json.dumps(issues, indent=2))


# this is the entry point used when this script is run directly
def main() -> None:
    # this fetches a small sample of real, live issues from home-assistant/core
    raw_issues = fetch_issues()
    # this simplifies every fetched issue down to just the fields we need
    simplified_issues = [simplify_issue(raw_issue) for raw_issue in raw_issues]
    # this saves the simplified issues locally so later stages don't need the network
    save_issues(simplified_issues)
    # this prints a friendly confirmation of how many issues were saved and where
    print(f"saved {len(simplified_issues)} issues to {settings.ISSUES_OUTPUT_PATH}")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off the ingestion
    main()
