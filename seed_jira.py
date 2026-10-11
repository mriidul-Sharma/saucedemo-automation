import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL", "").rstrip('/')
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_available_issue_types():
    """Fetches available issue types in the Jira project."""
    url = f"{JIRA_URL}/rest/api/2/issue/createmeta?projectKeys={PROJECT_KEY}"
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        data = response.json()
        projects = data.get("projects", [])
        if projects:
            return [it["name"] for it in projects[0].get("issuetypes", [])]
    return []

def create_issue(summary, description, issue_type="Story"):
    """Creates a new issue in Jira via the REST API."""
    url = f"{JIRA_URL}/rest/api/2/issue"
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code in [200, 201]:
        issue_key = response.json().get("key")
        print(f"✔ Ticket Created: [{issue_key}] - {summary}")
        return issue_key
    else:
        print(f"✖ Failed to create '{summary}': HTTP {response.status_code}")
        print(response.text)
        return None

def main():
    print("=" * 60)
    print(f"Connecting to Jira: {JIRA_URL} (Project: {PROJECT_KEY})")
    print("=" * 60)

    available_types = get_available_issue_types()
    print(f"Available Issue Types in {PROJECT_KEY}: {available_types}")

    # Use Xray 'Test' issue type if available; fallback to 'Task' if not configured
    test_type = "Test" if "Test" in available_types else "Task"

    # 1. Create the User Story
    story_summary = "[AUTH-01] User Authentication and Catalog Access for SauceDemo"
    story_desc = (
        "As a registered SauceDemo shopper,\n"
        "I want to securely log in with valid credentials,\n"
        "So that I can browse inventory and place orders.\n\n"
        "Acceptance Criteria:\n"
        "1. Valid credentials (standard_user) redirect to /inventory.html.\n"
        "2. Locked out user displays error: 'Epic sadface: Sorry, this user has been locked out.'\n"
        "3. Empty password displays error: 'Epic sadface: Password is required'."
    )
    create_issue(story_summary, story_desc, issue_type="Story")

    # 2. Define and create the Automation Test Cases
    test_cases = [
        (
            "[TC-01] Verify successful login with standard_user",
            "Objective: Ensure standard_user can log in successfully.\n"
            "Steps:\n"
            "1. Navigate to https://www.saucedemo.com\n"
            "2. Enter username 'standard_user'\n"
            "3. Enter password 'secret_sauce'\n"
            "4. Click Login\n"
            "Expected Result: Redirected to inventory.html and shopping cart icon is visible."
        ),
        (
            "[TC-02] Verify error banner for locked_out_user",
            "Objective: Verify error message when locked user attempts login.\n"
            "Steps:\n"
            "1. Navigate to https://www.saucedemo.com\n"
            "2. Enter username 'locked_out_user'\n"
            "3. Enter password 'secret_sauce'\n"
            "4. Click Login\n"
            "Expected Result: Error text displays 'Epic sadface: Sorry, this user has been locked out.'"
        ),
        (
            "[TC-03] Verify validation error when password is empty",
            "Objective: Verify field validation when password is omitted.\n"
            "Steps:\n"
            "1. Navigate to https://www.saucedemo.com\n"
            "2. Enter username 'standard_user'\n"
            "3. Leave password empty\n"
            "4. Click Login\n"
            "Expected Result: Error text displays 'Epic sadface: Password is required'."
        ),
        (
            "[TC-04] Verify end-to-end checkout flow",
            "Objective: Verify adding item to cart and completing checkout.\n"
            "Steps:\n"
            "1. Login as standard_user\n"
            "2. Add 'Sauce Labs Backpack' to cart\n"
            "3. Proceed to Checkout and fill details\n"
            "4. Click Finish\n"
            "Expected Result: Page displays 'Thank you for your order!'."
        )
    ]

    print("\nCreating Test Cases...")
    for summary, desc in test_cases:
        create_issue(summary, desc, issue_type=test_type)

    print("\n" + "=" * 60)
    print("Completed. Review your Jira Board at:")
    print(f"{JIRA_URL}/jira/software/projects/{PROJECT_KEY}/boards/1")
    print("=" * 60)

if __name__ == "__main__":
    main()