import os

import requests
from dotenv import load_dotenv


load_dotenv()


class JiraClient:
    """Client for creating and managing Jira incidents."""

    def __init__(self):
        self.jira_url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")

        if not all(
            [
                self.jira_url,
                self.email,
                self.api_token,
                self.project_key,
            ]
        ):
            raise ValueError(
                "Jira configuration is missing in .env"
            )

        self.jira_url = self.jira_url.rstrip("/")

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self.auth = (
            self.email,
            self.api_token,
        )

        self.timeout = 30

    # ==================================================
    # Find Existing Open Incident
    # ==================================================

    def find_existing_incident(self, pod_name: str):
        url = f"{self.jira_url}/rest/api/3/search/jql"

        jql = (
            f'project = "{self.project_key}" '
            f'AND summary ~ "\\"{pod_name}\\"" '
            f'AND statusCategory != Done '
            f'ORDER BY created DESC'
        )

        params = {
            "jql": jql,
            "maxResults": 1,
            "fields": "summary,status",
        }

        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        )

        response.raise_for_status()

        issues = response.json().get("issues", [])

        if issues:
            return issues[0]

        return None

    # ==================================================
    # Create Incident
    # ==================================================

    def create_incident(self, incident: dict):
        pod_name = incident["pod"]

        # ------------------------------------------------
        # Duplicate Check
        # ------------------------------------------------

        existing = self.find_existing_incident(
            pod_name
        )

        if existing:
            return self.update_incident(
                existing["key"],
                incident,
            )

        # ------------------------------------------------
        # Create New Jira Issue
        # ------------------------------------------------

        url = f"{self.jira_url}/rest/api/3/issue"

        description = (
            "Kubernetes Incident\n\n"
            f"Pod: {incident['pod']}\n"
            f"Namespace: {incident['namespace']}\n"
            f"Status: {incident['status']}\n\n"
            "AI Analysis:\n"
            f"{incident['analysis']}"
        )

        payload = {
            "fields": {
                "project": {
                    "key": self.project_key,
                },
                "summary": (
                    f"[Kubernetes Incident] "
                    f"{incident['pod']}"
                ),
                "issuetype": {
                    "name": "Task",
                },
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description,
                                }
                            ],
                        }
                    ],
                },
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        )

        response.raise_for_status()

        result = response.json()

        return {
            "created": True,
            "duplicate": False,
            "key": result.get("key"),
            "id": result.get("id"),
            "self": result.get("self"),
        }

    # ==================================================
    # Update Existing Incident
    # ==================================================

    def update_incident(
        self,
        issue_key: str,
        incident: dict,
    ):
        message = (
            "Kubernetes Incident Update\n\n"
            f"Pod: {incident['pod']}\n"
            f"Namespace: {incident['namespace']}\n"
            f"Status: {incident['status']}\n\n"
            "AI Analysis:\n"
            f"{incident['analysis']}"
        )

        result = self.add_comment(
            issue_key,
            message,
        )

        return {
            "created": False,
            "duplicate": True,
            "updated": True,
            "key": issue_key,
            "id": None,
            "comment_id": result.get("comment_id"),
            "message": (
                "Existing Jira incident found. "
                "New ticket was not created."
            ),
        }

    # ==================================================
    # Add Comment
    # ==================================================

    def add_comment(
        self,
        issue_key: str,
        message: str,
    ):
        url = (
            f"{self.jira_url}/rest/api/3/issue/"
            f"{issue_key}/comment"
        )

        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": message,
                            }
                        ],
                    }
                ],
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        )

        response.raise_for_status()

        result = response.json()

        return {
            "commented": True,
            "key": issue_key,
            "comment_id": result.get("id"),
            "message": "Jira comment added successfully.",
        }

    # ==================================================
    # Get Transitions
    # ==================================================

    def get_transitions(self, issue_key: str):
        url = (
            f"{self.jira_url}/rest/api/3/issue/"
            f"{issue_key}/transitions"
        )

        response = requests.get(
            url,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    # ==================================================
    # Resolve Incident
    # ==================================================

    def resolve_incident(
        self,
        issue_key: str,
        resolution_message: str,
    ):
        transitions_data = self.get_transitions(
            issue_key
        )

        resolved_transition = None

        for transition in transitions_data.get(
            "transitions",
            [],
        ):
            if transition["name"].lower() == "resolved":
                resolved_transition = transition
                break

        if not resolved_transition:
            raise ValueError(
                f"Resolved transition not available "
                f"for Jira issue {issue_key}"
            )

        transition_id = resolved_transition["id"]

        # ------------------------------------------------
        # Perform Jira Transition
        # ------------------------------------------------

        url = (
            f"{self.jira_url}/rest/api/3/issue/"
            f"{issue_key}/transitions"
        )

        payload = {
            "transition": {
                "id": transition_id,
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        )

        response.raise_for_status()

        # ------------------------------------------------
        # Add Resolution Comment
        # ------------------------------------------------

        self.add_comment(
            issue_key,
            resolution_message,
        )

        return {
            "resolved": True,
            "key": issue_key,
            "transition_id": transition_id,
            "message": (
                "Jira incident resolved successfully."
            ),
        }