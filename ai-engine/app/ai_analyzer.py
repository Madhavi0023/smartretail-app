import requests

from app.config import settings


class AIAnalyzer:
    """Analyze Kubernetes incidents using deterministic rules and Ollama."""

    def __init__(
        self,
        ollama_url: str = None,
        model: str = None,
    ):
        self.ollama_url = (
            ollama_url or settings.OLLAMA_URL
        ).rstrip("/")

        self.model = (
            model or settings.OLLAMA_MODEL
        )

    def analyze(
        self,
        pod_status,
        logs,
        events,
    ):
        """
        Analyze a Kubernetes incident.

        Known Kubernetes conditions are handled deterministically.
        Other incidents are analyzed by the local Ollama model.
        """

        # --------------------------------------------------
        # Deterministic Kubernetes Evidence
        # --------------------------------------------------

        events_text = str(events)

        if (
            "FailedScheduling" in events_text
            and "Too many pods" in events_text
        ):
            if "No preemption victims found" in events_text:
                preemption_info = (
                    "Kubernetes could not find an existing "
                    "pod suitable for preemption."
                )
            else:
                preemption_info = (
                    "Preemption information was not provided."
                )

            return (
                "Severity: Medium\n"
                "Root Cause: The available node has reached "
                "its pod capacity.\n"
                "Evidence: Kubernetes event Reason is "
                "FailedScheduling and the event message "
                "contains \"Too many pods\". "
                f"{preemption_info}\n"
                "Recommended Action: Review node pod capacity "
                "and available cluster capacity before making "
                "any production change.\n"
                "Auto-Remediation Possible: No\n"
                "Confidence: High"
            )

        # --------------------------------------------------
        # AI Analysis for Other Incidents
        # --------------------------------------------------

        prompt = f"""
You are a Kubernetes Production SRE.

Analyze the Kubernetes incident using ONLY the evidence
provided below.

STRICT RULES:

1. Never invent or assume information.
2. Do not create logs, events, metrics, errors,
   commands, or configuration problems that are not present.
3. Kubernetes EVENTS are the primary evidence for
   scheduling problems.
4. POD STATUS shows the current state but does not
   by itself explain the root cause.
5. If an event contains FailedScheduling, use that
   event as the primary evidence.
6. If evidence is insufficient, state:
   "Insufficient evidence to determine the root cause."
7. Do not assume CPU, memory, networking, or configuration
   problems unless the evidence explicitly shows them.
8. Do not claim a namespace has a capacity problem when
   the evidence refers to node capacity.
9. Do not recommend deleting pods unless the evidence
   explicitly supports it.
10. Do not perform or suggest risky production changes
    without human approval.
11. Auto-remediation must be "No" unless the evidence
    clearly supports a safe automated action.
12. Keep the analysis concise and factual.
13. FailedScheduling events MUST be treated as relevant
    evidence.
14. "Too many pods" means node pod-capacity exhaustion.
15. Do not say that the namespace has too many pods.
16. Do not say that pods are simply waiting for nodes.
17. Do not recommend rolling updates unless the evidence
    explicitly shows a rollout problem.
18. Do not recommend changing pod specifications unless
    the evidence explicitly shows a pod-specification problem.
19. If the event says "No preemption victims found",
    explain that Kubernetes could not find an existing
    pod suitable for preemption.
20. Confidence MUST be exactly one of:
    High, Medium, Low.
21. Auto-Remediation Possible MUST be exactly one of:
    Yes, No.

POD STATUS:
{pod_status}

POD LOGS:
{logs}

KUBERNETES EVENTS:
{events}

Return ONLY:

Severity:
Root Cause:
Evidence:
Recommended Action:
Auto-Remediation Possible:
Confidence:
"""

        # --------------------------------------------------
        # Ollama Request
        # --------------------------------------------------

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            return (
                "Severity: Unknown\n"
                "Root Cause: AI analysis unavailable.\n"
                f"Evidence: Ollama request failed: {exc}\n"
                "Recommended Action: Review Ollama service "
                "availability and retry the analysis.\n"
                "Auto-Remediation Possible: No\n"
                "Confidence: Low"
            )

        data = response.json()

        analysis = data.get("response")

        if not analysis:
            return (
                "Severity: Unknown\n"
                "Root Cause: AI analysis returned no result.\n"
                "Evidence: Ollama returned an empty response.\n"
                "Recommended Action: Retry the analysis.\n"
                "Auto-Remediation Possible: No\n"
                "Confidence: Low"
            )

        return analysis.strip()