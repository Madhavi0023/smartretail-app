from typing import Optional

from kubernetes import client


class LogCollector:
    """Collect logs from Kubernetes Pods."""

    def __init__(self, core_api: client.CoreV1Api):
        self.core_api = core_api

    def get_pod_logs(
        self,
        pod_name: str,
        namespace: str = "default",
        tail_lines: int = 100,
    ) -> str:
        """
        Retrieve the latest logs from a Kubernetes Pod.

        Returns a readable message when logs are unavailable
        instead of failing the complete incident analysis.
        """

        try:
            logs = self.core_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                tail_lines=tail_lines,
            )

        except Exception as exc:
            return (
                f"Pod logs unavailable for "
                f"{namespace}/{pod_name}: {exc}"
            )

        if isinstance(logs, bytes):
            return logs.decode(
                "utf-8",
                errors="replace",
            )

        return logs or ""