from datetime import datetime, timezone

from kubernetes import client, config


class KubernetesClient:
    """Client wrapper for Kubernetes API operations."""

    def __init__(self):
        config.load_kube_config()

        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()

    # --------------------------------------------------
    # Pods
    # --------------------------------------------------

    def get_pods(self, namespace: str = "default"):
        """Return basic information about pods in a namespace."""

        pods = self.core_api.list_namespaced_pod(
            namespace=namespace
        )

        return [
            {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
            }
            for pod in pods.items
        ]

    # --------------------------------------------------
    # Pod → Deployment
    # --------------------------------------------------

    def get_pod_deployment(
        self,
        pod_name: str,
        namespace: str = "default",
    ):
        """Find the Deployment that owns a given Pod."""

        pod = self.core_api.read_namespaced_pod(
            name=pod_name,
            namespace=namespace,
        )

        owner_references = pod.metadata.owner_references or []

        if not owner_references:
            return None

        owner = owner_references[0]

        # Pod directly owned by Deployment
        if owner.kind == "Deployment":
            return owner.name

        # Normally Pod → ReplicaSet → Deployment
        if owner.kind == "ReplicaSet":
            replicaset = (
                self.apps_api.read_namespaced_replica_set(
                    name=owner.name,
                    namespace=namespace,
                )
            )

            rs_owners = (
                replicaset.metadata.owner_references or []
            )

            if not rs_owners:
                return None

            rs_owner = rs_owners[0]

            if rs_owner.kind == "Deployment":
                return rs_owner.name

        return None

    # --------------------------------------------------
    # Deployment Restart
    # --------------------------------------------------

    def rollout_restart(
        self,
        deployment_name: str,
        namespace: str = "default",
    ):
        """
        Trigger a Kubernetes Deployment rollout restart.

        This method is available for future controlled
        remediation and is not automatically executed by
        the incident detection flow.
        """

        deployment = (
            self.apps_api.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
            )
        )

        if deployment.spec.template.metadata.annotations is None:
            deployment.spec.template.metadata.annotations = {}

        deployment.spec.template.metadata.annotations[
            "kubectl.kubernetes.io/restartedAt"
        ] = datetime.now(
            timezone.utc
        ).isoformat()

        self.apps_api.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment,
        )

        return {
            "restarted": True,
            "deployment": deployment_name,
            "namespace": namespace,
        }

    # --------------------------------------------------
    # Deployment Health
    # --------------------------------------------------

    def verify_deployment(
        self,
        deployment_name: str,
        namespace: str = "default",
    ):
        """Check whether desired Deployment replicas are healthy."""

        deployment = (
            self.apps_api.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
            )
        )

        desired = deployment.spec.replicas or 0
        ready = deployment.status.ready_replicas or 0
        available = deployment.status.available_replicas or 0

        healthy = (
            desired > 0
            and ready == desired
            and available == desired
        )

        return {
            "healthy": healthy,
            "deployment": deployment_name,
            "namespace": namespace,
            "desired_replicas": desired,
            "ready_replicas": ready,
            "available_replicas": available,
        }