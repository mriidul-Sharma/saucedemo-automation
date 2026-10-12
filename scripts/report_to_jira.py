import os
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth

# Jira Cloud Configuration
JIRA_DOMAIN = "mridulsharma1206.atlassian.net"
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# Mapping test functions to your Jira issue keys
TEST_MAPPING = {
    "test_tc01_valid_login": "SCRUM-6",
    "test_tc02_locked_out_user": "SCRUM-7",
    "test_tc03_empty_password": "SCRUM-8",
}

def post_comment_to_jira(issue_key, comment_text):
    url = f"https://{JIRA_DOMAIN}/rest/api/2/issue/{issue_key}/comment"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Content-Type": "application/json"}
    payload = {"body": comment_text}

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 201:
        print(f"Successfully posted status to {issue_key}")
    else:
        print(f"Failed to post to {issue_key}: {response.status_code} - {response.text}")

def parse_and_report():
    xml_path = "reports/test-results.xml"
    if not os.path.exists(xml_path):
        print(f"Report file {xml_path} not found.")
        return

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate through test cases in the JUnit XML
    for testcase in root.iter("testcase"):
        test_name = testcase.attrib.get("name")
        failure = testcase.find("failure")
        error = testcase.find("error")

        if failure is not None or error is not None:
            status = "FAILED"
            details = failure.attrib.get("message") if failure is not None else "Execution Error"
        else:
            status = "PASSED"
            details = "All assertions passed successfully."

        # Find matching Jira key and post comment
        issue_key = TEST_MAPPING.get(test_name)
        if issue_key:
            comment = (
                f"Test: {test_name}\n"
                f"Status: {status}\n"
                f"Details: {details}\n"
                f"Build Runner: GitHub Cloud Ubuntu"
            )
            post_comment_to_jira(issue_key, comment)

if __name__ == "__main__":
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print("Missing JIRA_EMAIL or JIRA_API_TOKEN environment variables.")
    else:
        parse_and_report()