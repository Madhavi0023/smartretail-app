from app.config import settings
from app.kubernetes_client import KubernetesClient


class IncidentDetector:
    """Detect Kubernetes pod and container-level incidents."""

    POD_INCIDENT_STATUSES = {
        "Pending",
        "Failed",
        "Unknown",
    }

    CONTAINER_INCIDENT_REASONS = {
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "ErrImagePull",
        "CreateContainerConfigError",
    }

    def __init__(self):
        self.k8s = KubernetesClient()

    def detect(self, namespace: str = None):
        """
        Detect incidents from Kubernetes Pods.

        A Pod generates at most one incident record.
        Container-level problems are included in that record
        when present.
        """

        namespace = namespace or settings.KUBERNETES_NAMESPACE

        pods = self.k8s.core_api.list_namespaced_pod(
            namespace=namespace
        )

        incidents = []

        for pod in pods.items:
            pod_status = pod.status.phase

            container_problems = []

            container_statuses = (
                pod.status.container_statuses or []
            )

            for container in container_statuses:
                waiting_state = container.state.waiting

                if not waiting_state:
                    continue

                reason = waiting_state.reason

                if reason in self.CONTAINER_INCIDENT_REASONS:
                    container_problems.append(
                        {
                            "container": container.name,
                            "reason": reason,
                        }
                    )

            # Pod-level incident
            if pod_status in self.POD_INCIDENT_STATUSES:
                incident = {
                    "pod": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod_status,
                }

                if container_problems:
                    incident["container_problems"] = (
                        container_problems
                    )

                incidents.append(incident)

                continue

            # Container-level incident for otherwise healthy Pod
            if container_problems:
                incidents.append(
                    {
                        "pod": pod.metadata.name,
                        "namespace": pod.metadata.namespace,
                        "status": pod_status,
                        "container_problems": container_problems,
                    }
                )

        return incidents