from app.kubernetes_client import KubernetesClient
from app.log_collector import LogCollector
from app.event_collector import EventCollector
from app.ai_analyzer import AIAnalyzer
from app.jira_client import JiraClient
from app.notification_service import NotificationService


class IncidentService:
    """Orchestrate the complete Kubernetes incident workflow."""

    def __init__(self):
        self.k8s = KubernetesClient()
        self.analyzer = AIAnalyzer()
        self.jira = JiraClient()
        self.notification = NotificationService()

    def analyze_pod(
        self,
        pod_name: str,
        namespace: str = "default",
    ):
        # ==================================================
        # 1. Get Pod Status
        # ==================================================

        pod = self.k8s.core_api.read_namespaced_pod(
            name=pod_name,
            namespace=namespace,
        )

        pod_status = {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
        }

        # ==================================================
        # 2. Collect Pod Logs
        # ==================================================

        log_collector = LogCollector(
            self.k8s.core_api
        )

        logs = log_collector.get_pod_logs(
            pod_name=pod_name,
            namespace=namespace,
        )

        # ==================================================
        # 3. Collect Kubernetes Events
        # ==================================================

        event_collector = EventCollector(
            self.k8s.core_api
        )

        events = event_collector.get_pod_events(
            pod_name=pod_name,
            namespace=namespace,
        )

        # ==================================================
        # 4. AI Root Cause Analysis
        # ==================================================

        analysis = self.analyzer.analyze(
            pod_status=pod_status,
            logs=logs,
            events=events,
        )

        # ==================================================
        # 5. Build Incident
        # ==================================================

        incident = {
            "pod": pod_name,
            "namespace": namespace,
            "status": pod.status.phase,
            "analysis": analysis,
        }

        # ==================================================
        # 6. Create / Update Jira Incident
        # ==================================================

        jira_result = self.jira.create_incident(
            incident
        )

        # ==================================================
        # 7. Send Email Notification
        # ==================================================

        notification_result = (
            self.notification.send_incident_notification(
                incident=incident,
                jira_result=jira_result,
            )
        )

        # ==================================================
        # 8. Final Incident Result
        # ==================================================

        return {
            "pod": pod_name,
            "namespace": namespace,
            "pod_status": pod_status,
            "logs": logs,
            "events": events,
            "analysis": analysis,
            "jira": {
                "key": jira_result.get("key"),
                "id": jira_result.get("id"),
                "created": jira_result.get("created"),
                "duplicate": jira_result.get("duplicate"),
                "updated": jira_result.get("updated"),
            },
            "notification": notification_result,
        }