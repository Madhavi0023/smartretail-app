# SmartRetail AI DevOps Platform

An end-to-end DevOps and AI-powered incident management platform for deploying, monitoring, analyzing, and troubleshooting a containerized SmartRetail application on AWS and Kubernetes.

The platform combines AWS infrastructure, Docker, Kubernetes, Helm, CI/CD, security scanning, observability, and an AI-powered incident response engine.

---

## Project Overview

SmartRetail is a production-style DevOps project designed to demonstrate how a modern application can be:

- Containerized using Docker
- Deployed on Amazon EKS
- Managed using Helm
- Automated using CI/CD
- Secured using DevSecOps tools
- Monitored through Kubernetes observability tools
- Analyzed using an AI-powered incident engine
- Integrated with Jira for incident management
- Notified through email

The main goal is to reduce manual incident investigation by automatically collecting Kubernetes evidence and generating an actionable root-cause analysis.

---

## Architecture

```text
                    Developer
                       |
                       v
                    GitHub
                       |
                       v
               GitHub Actions CI/CD
                       |
          +------------+-------------+
          |                          |
          v                          v
     Security Scan              Docker Build
   SonarQube / Trivy                  |
          |                           v
          +-----------------------> ECR
                                      |
                                      v
                                  Amazon EKS
                                      |
                         +------------+------------+
                         |                         |
                         v                         v
                    Kubernetes                Helm
                    Deployment                Release
                         |
                         v
                    SmartRetail
                    Application
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Logs           Events         Metrics
          |              |              |
          +--------------+--------------+
                         |
                         v
                AI DevOps Engine
                         |
                    AI / Ollama
                         |
              +----------+----------+
              |                     |
              v                     v
            Jira                  Email
           Incident              Alert

           #Tech Stack 
           | Category            | Technologies                                |
| ------------------- | ------------------------------------------- |
| Cloud               | AWS                                         |
| Infrastructure      | Terraform                                   |
| Compute             | Amazon EKS                                  |
| Networking          | VPC, Subnets, NAT Gateway, Internet Gateway |
| Containerization    | Docker                                      |
| Container Registry  | Amazon ECR                                  |
| Orchestration       | Kubernetes                                  |
| Package Management  | Helm                                        |
| CI/CD               | GitHub Actions                              |
| Security            | SonarQube, Trivy, OWASP Dependency-Check    |
| Monitoring          | Prometheus, Grafana                         |
| AI                  | Ollama, Qwen 2.5 0.5B                       |
| Backend             | FastAPI                                     |
| Incident Management | Jira                                        |
| Notifications       | SMTP / Gmail                                |
| Language            | Python                                      |
| OS / Tools          | Linux, Shell, Git                           |
############Project structure 
smartretail-app/
│
├── ai-engine/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── kubernetes_client.py
│   │   ├── incident_detector.py
│   │   ├── incident_service.py
│   │   ├── log_collector.py
│   │   ├── event_collector.py
│   │   ├── ai_analyzer.py
│   │   ├── jira_client.py
│   │   ├── notification_service.py
│   │   ├── prometheus_client.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
├── backend/
│
├── frontend/
│
├── helm/
│
├── terraform/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .gitignore
└── README.md

Infrastructure

The infrastructure is provisioned using Terraform.

The AWS environment includes components such as:

AWS VPC
 |
 +-- Public Subnets
 |
 +-- Private Subnets
 |
 +-- NAT Gateway
 |
 +-- Internet Gateway
 |
 +-- Amazon EKS
 |
 +-- RDS
 |
 +-- Redis
 |
 +-- Application Load Balancer
 |
 +-- Amazon ECR

Terraform allows the infrastructure to be created and destroyed consistently.

Kubernetes Deployment

The SmartRetail application is deployed to Amazon EKS.

The deployment uses:

Kubernetes Deployments
Services
ConfigMaps / Secrets
Ingress
Helm Charts
Horizontal Pod Autoscaler
AWS Load Balancer Controller

Example:

kubectl get pods -n default
kubectl get deployments -n default
kubectl get services -n default
Helm

The application is packaged and deployed using Helm.

Helm provides:

Reusable Kubernetes templates
Environment-specific configuration
Image tag management
Replica configuration
Service configuration
Ingress configuration
Autoscaling configuration

Example:

helm lint .
helm template smartretail .
helm upgrade --install smartretail .
CI/CD

GitHub Actions automates the application delivery pipeline.

Typical workflow:

Git Push
   |
   v
GitHub Actions
   |
   +--> Code Quality
   |
   +--> Security Scan
   |
   +--> Docker Build
   |
   +--> Push Image to ECR
   |
   +--> Deploy using Helm
   |
   v
Amazon EKS
DevSecOps

Security is integrated into the CI/CD workflow.

Tools include:

SonarQube

Used for:

Code quality
Code smells
Maintainability
Static analysis
Trivy

Used for:

Container vulnerability scanning
Dependency vulnerability detection
Security checks
OWASP Dependency-Check

Used to identify vulnerable application dependencies.

AI DevOps Incident Engine

The AI engine is the main intelligent component of the project.

It automatically detects Kubernetes incidents and performs root-cause analysis.

Incident Flow
Kubernetes
     |
     v
Incident Detector
     |
     v
Unhealthy Pod
     |
     +----> Pod Status
     |
     +----> Pod Logs
     |
     +----> Kubernetes Events
     |
     v
AI Analyzer
     |
     v
Root Cause Analysis
     |
     +----> Jira Incident
     |
     +----> Email Notification
AI Analysis

The AI engine currently uses:

Ollama
   +
Qwen 2.5 0.5B

The AI receives Kubernetes evidence and generates:

Severity
Root Cause
Evidence
Recommended Action
Auto-Remediation Possible
Confidence

The system follows an evidence-first approach.

It does not blindly assume:

CPU problems
Memory problems
Network problems
Configuration problems

unless Kubernetes evidence supports the conclusion.

Example Incident

Suppose Kubernetes reports:

Warning  FailedScheduling


0/1 nodes are available:
1 Too many pods.


No preemption victims found.

The AI engine identifies:

Severity: Medium


Root Cause:
The available node has reached its pod capacity.


Evidence:
FailedScheduling - Too many pods.


Recommended Action:
Review node pod capacity and available cluster capacity.


Auto-Remediation Possible:
No


Confidence:
High
Jira Integration

The AI engine integrates with Jira to automatically manage incidents.

The workflow supports:

New Incident
     |
     v
Search Existing Jira Incident
     |
     +---- Existing ----> Add Comment / Update
     |
     +---- Not Existing -> Create Ticket

This prevents duplicate Jira incidents for the same active Kubernetes problem.

Example:

SRAI-5
Email Notifications

After Jira processing, the system sends an email notification containing:

Pod name
Namespace
Status
AI root-cause analysis
Recommended action
Jira ticket

Example:

Kubernetes Incident Alert


Pod: smartretail-test-pod
Namespace: default
Status: Pending


AI Analysis:
Severity: Medium
Root Cause: The available node has reached its pod capacity.
Evidence: FailedScheduling - Too many pods.
Confidence: High


Jira Ticket: SRAI-5
FastAPI AI Engine

The AI engine exposes REST APIs using FastAPI.

Start the application:

uvicorn app.main:app --reload --port 8000

Swagger documentation:

http://127.0.0.1:8000/docs
Important API Endpoints
Service Health
GET /
GET /health
Kubernetes
GET /kubernetes/pods
GET /kubernetes/logs/{namespace}/{pod_name}
GET /kubernetes/events/{namespace}/{pod_name}
AI Analysis

Analyze one Pod:

GET /kubernetes/analyze/{namespace}/{pod_name}

Detect incidents:

GET /kubernetes/incidents

Run the complete automation workflow:

GET /kubernetes/incidents/analyze

The complete workflow is:

Kubernetes
    ↓
Incident Detection
    ↓
Logs + Events
    ↓
AI RCA
    ↓
Jira
    ↓
Email
Production Safety

The current AI engine follows a human-approval approach for production remediation.

The AI can:

Detect incidents
Analyze evidence
Recommend actions
Create/update Jira incidents
Notify engineers

It does not automatically execute risky production changes unless a future remediation policy explicitly allows a safe action.

This approach reduces the risk of unintended production changes.

Security

Sensitive credentials are stored in environment variables.

Example:

.env

The .env file is excluded from Git using .gitignore.

Never commit:

Jira API tokens
Gmail app passwords
AWS credentials
Kubernetes credentials
Other secrets

Use .env.example when sharing configuration structure.

Running the AI Engine Locally
1. Create virtual environment
python -m venv venv
2. Activate

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate
3. Install dependencies
pip install -r ai-engine/requirements.txt
4. Start Ollama
ollama serve
5. Verify model
ollama list
6. Start FastAPI
uvicorn app.main:app --reload --port 8000
Interview Demo

The complete project can be demonstrated using the following flow:

1. Show Kubernetes Pods
        ↓
2. Show unhealthy / Pending Pod
        ↓
3. Show Kubernetes event
        ↓
4. Show FailedScheduling evidence
        ↓
5. Open FastAPI Swagger
        ↓
6. Run /kubernetes/incidents/analyze
        ↓
7. Show AI Root Cause Analysis
        ↓
8. Show Jira Incident
        ↓
9. Show Email Notification

This demonstrates the complete automated incident-management workflow.

Current Implementation

The currently completed AI incident workflow is:

Kubernetes
    ↓
Incident Detection
    ↓
Pod Status
    ↓
Logs
    ↓
Kubernetes Events
    ↓
Qwen AI Analysis
    ↓
Jira Create / Update
    ↓
Email Notification
Future Enhancements

Planned enhancements include:

Prometheus metric analysis
Grafana dashboards
AWS CloudWatch integration
Terraform context analysis
GitHub Actions log analysis
SonarQube report analysis
Trivy report analysis
Incident correlation
Historical incident learning
Slack / Teams notifications
Controlled production auto-remediation
Advanced alert deduplication
Project Objective

The objective of SmartRetail AI DevOps Platform is to demonstrate how AI can assist DevOps/SRE teams in identifying and troubleshooting production-style Kubernetes incidents.

Instead of manually checking multiple systems:

kubectl
Logs
Events
Jira
Email

the AI DevOps engine brings the incident investigation workflow together:

Detect
  ↓
Collect Evidence
  ↓
Analyze
  ↓
Create Incident
  ↓
Notify
  ↓
Human Review
Author

Madhavi Sharma

DevOps Engineer



**Isko root `README.md` mein rakho.**


Tumhare paas phir:


```text
root README.md
        ↓
Complete project overview


ai-engine/README.md
        ↓
Detailed AI engine documentation
