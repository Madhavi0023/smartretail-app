from fastapi import FastAPI, HTTPException

from app.kubernetes_client import KubernetesClient
from app.log_collector import LogCollector
from app.event_collector import EventCollector
from app.incident_detector import IncidentDetector
from app.incident_service import IncidentService
from app.jira_client import JiraClient


app = FastAPI(
    title="SmartRetail AI DevOps Engine",
    description=(
        "AI-powered Kubernetes incident detection, "
        "root-cause analysis, Jira incident management "
        "and email notification"
    ),
    version="1.0.0",
)


# ==========================================================
# Health & Service Information
# ==========================================================


@app.get("/")
def root():
    return {
        "service": "smartretail-ai-engine",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ==========================================================
# Kubernetes
# ==========================================================


@app.get("/kubernetes/pods")
def get_pods():
    try:
        k8s = KubernetesClient()

        return {
            "pods": k8s.get_pods(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve Kubernetes pods: {exc}",
        )


@app.get("/kubernetes/logs/{namespace}/{pod_name}")
def get_logs(
    namespace: str,
    pod_name: str,
):
    try:
        k8s = KubernetesClient()

        collector = LogCollector(
            k8s.core_api
        )

        logs = collector.get_pod_logs(
            pod_name=pod_name.strip(),
            namespace=namespace.strip(),
        )

        return {
            "pod": pod_name,
            "namespace": namespace,
            "logs": logs,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve pod logs: {exc}",
        )


@app.get("/kubernetes/events/{namespace}/{pod_name}")
def get_events(
    namespace: str,
    pod_name: str,
):
    try:
        k8s = KubernetesClient()

        collector = EventCollector(
            k8s.core_api
        )

        events = collector.get_pod_events(
            pod_name=pod_name.strip(),
            namespace=namespace.strip(),
        )

        return {
            "pod": pod_name,
            "namespace": namespace,
            "events": events,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve pod events: {exc}",
        )


# ==========================================================
# Single Pod Incident Analysis
# ==========================================================


@app.get("/kubernetes/analyze/{namespace}/{pod_name}")
def analyze_pod(
    namespace: str,
    pod_name: str,
):
    """
    Analyze a single Kubernetes Pod.

    Flow:
    Pod → Logs → Events → AI RCA
    """

    namespace = namespace.strip()
    pod_name = pod_name.strip()

    try:
        service = IncidentService()

        result = service.analyze_pod(
            pod_name=pod_name,
            namespace=namespace,
        )

        return {
            "pod": pod_name,
            "namespace": namespace,
            "pod_status": result["pod_status"],
            "analysis": result["analysis"],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Pod analysis failed: {exc}",
        )


# ==========================================================
# Incident Detection
# ==========================================================


@app.get("/kubernetes/incidents")
def detect_incidents():
    """
    Detect currently unhealthy Kubernetes Pods.

    This endpoint only detects incidents.
    It does not create Jira tickets or send emails.
    """

    try:
        detector = IncidentDetector()

        incidents = detector.detect()

        return {
            "incident_count": len(incidents),
            "incidents": incidents,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Incident detection failed: {exc}",
        )


# ==========================================================
# Complete Incident Automation
# ==========================================================


@app.get("/kubernetes/incidents/analyze")
def analyze_incidents():
    """
    Run the complete incident automation workflow.

    Flow:
    Kubernetes
        ↓
    Incident Detection
        ↓
    Logs + Events
        ↓
    AI Root Cause Analysis
        ↓
    Jira Create / Update
        ↓
    Email Notification
    """

    try:
        detector = IncidentDetector()

        incidents = detector.detect()

        service = IncidentService()

        results = []

        for incident in incidents:

            result = service.analyze_pod(
                pod_name=incident["pod"],
                namespace=incident["namespace"],
            )

            results.append(
                {
                    "pod": incident["pod"],
                    "namespace": incident["namespace"],
                    "status": incident["status"],
                    "analysis": result["analysis"],
                    "jira": result["jira"],
                    "notification": result["notification"],
                }
            )

        return {
            "incident_count": len(results),
            "incidents": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Incident automation failed: {exc}",
        )


# ==========================================================
# Jira Test Endpoint
# ==========================================================


@app.post("/jira/test")
def jira_test():
    """
    Test Jira connectivity and incident creation.
    """

    try:
        jira = JiraClient()

        incident = {
            "pod": "smartretail-test-pod",
            "namespace": "default",
            "status": "Pending",
            "analysis": (
                "Severity: Medium\n"
                "Root Cause: The available node has "
                "reached its pod capacity.\n"
                "Evidence: FailedScheduling - "
                "Too many pods.\n"
                "Recommended Action: Review node pod capacity "
                "and available cluster capacity.\n"
                "Auto-Remediation Possible: No\n"
                "Confidence: High"
            ),
        }

        result = jira.create_incident(
            incident
        )

        return {
            "message": "Jira test completed successfully",
            "jira": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Jira test failed: {exc}",
        )