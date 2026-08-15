from app.jira_client import JiraClient


jira = JiraClient()

result = jira.add_comment(
    "SRAI-4",
    "Test comment: AI detected that the incident "
    "has been investigated successfully."
)

print(result)