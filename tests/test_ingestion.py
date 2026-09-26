# we need our own settings so the test doesn't hardcode repo/branch values twice
from src.config import settings

# we need the doc-fetching module to test its pure URL-building logic
from src.ingestion import fetch_docs

# we need the issue-fetching module to test its pure issue-simplifying logic
from src.ingestion import fetch_issues


# this test checks that build_doc_url points at the real Home Assistant docs repo and branch
def test_build_doc_url_uses_configured_repo_and_branch() -> None:
    # this calls the function under test with a made-up slug so we control the expected output
    url = fetch_docs.build_doc_url("mqtt")
    # this checks the URL contains the configured docs repo name
    assert settings.DOCS_REPO in url
    # this checks the URL contains the configured docs branch name
    assert settings.DOCS_REPO_BRANCH in url
    # this checks the URL ends with the expected markdown file name for this slug
    assert url.endswith("source/_integrations/mqtt.markdown")


# this test checks that simplify_issue keeps only the fields we actually need
def test_simplify_issue_extracts_expected_fields() -> None:
    # this is a fake raw issue shaped like what GitHub's real API returns
    raw_issue = {
        "number": 42,
        "title": "Lights don't turn off",
        "body": "Detailed steps to reproduce.",
        "state": "open",
        "html_url": "https://github.com/home-assistant/core/issues/42",
        "pull_request": None,
    }
    # this calls the function under test
    simplified = fetch_issues.simplify_issue(raw_issue)
    # this checks every expected field made it through with the right value
    assert simplified == {
        "id": 42,
        "title": "Lights don't turn off",
        "body": "Detailed steps to reproduce.",
        "state": "open",
        "url": "https://github.com/home-assistant/core/issues/42",
    }


# this test checks that a missing body doesn't crash simplify_issue and becomes an empty string
def test_simplify_issue_handles_missing_body() -> None:
    # this is a raw issue with no "body" key at all, which real GitHub issues sometimes have
    raw_issue = {
        "number": 7,
        "title": "No description provided",
        "state": "closed",
        "html_url": "https://github.com/home-assistant/core/issues/7",
    }
    # this calls the function under test
    simplified = fetch_issues.simplify_issue(raw_issue)
    # this checks the missing body was safely defaulted to an empty string
    assert simplified["body"] == ""
