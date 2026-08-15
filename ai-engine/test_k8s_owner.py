from app.kubernetes_client import KubernetesClient


k8s = KubernetesClient()

result = k8s.verify_deployment(
    deployment_name="smartretail",
    namespace="default",
)

print(result)