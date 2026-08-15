from kubernetes import client


class EventCollector:
    """Collect Kubernetes Events associated with a Pod."""

    def __init__(self, core_api: client.CoreV1Api):
        self.core_api = core_api

    def get_pod_events(
        self,
        pod_name: str,
        namespace: str = "default",
    ):
        """
        Retrieve Kubernetes Events for a specific Pod.

        Events are used as primary evidence during
        incident analysis.
        """

        try:
            events = self.core_api.list_namespaced_event(
                namespace=namespace
            )
        except Exception as exc:
            return [
                {
                    "Type": "Warning",
                    "Reason": "EventCollectionError",
                    "Count": 1,
                    "From": "Kubernetes API",
                    "Message": (
                        f"Unable to collect events for "
                        f"{namespace}/{pod_name}: {exc}"
                    ),
                    "FirstTimestamp": None,
                    "LastTimestamp": None,
                }
            ]

        result = []

        for event in events.items:

            involved_object = event.involved_object

            if (
                not involved_object
                or involved_object.name != pod_name
            ):
                continue

            source = event.source

            result.append(
                {
                    "Type": event.type,
                    "Reason": event.reason,
                    "Count": event.count or 0,
                    "From": (
                        source.component
                        if source
                        else None
                    ),
                    "Message": event.message,
                    "FirstTimestamp": (
                        str(event.first_timestamp)
                        if event.first_timestamp
                        else None
                    ),
                    "LastTimestamp": (
                        str(event.last_timestamp)
                        if event.last_timestamp
                        else None
                    ),
                }
            )

        return result