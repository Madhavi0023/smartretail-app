from app.notification_service import NotificationService


notification = NotificationService()

incident = {
    "pod": "smartretail-test-pod",
    "namespace": "default",
    "status": "Pending",
    "analysis": (
        "Severity: Medium\n"
        "Root Cause: The available node has reached its pod capacity.\n"
        "Evidence: FailedScheduling - Too many pods.\n"
        "Recommended Action: Review node pod capacity.\n"
        "Auto-Remediation Possible: No\n"
        "Confidence: High"
    ),
}

jira_result = {
    "key": "SRAI-TEST",
}

result = notification.send_incident_notification(
    incident=incident,
    jira_result=jira_result,
)

print(result)