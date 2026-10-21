# CCA 2 — Student Task Tracker

Small Flask web application for the Jenkins CI/CD assessment.

## Pipeline
1. Jenkins checks out this GitHub repository.
2. Installs dependencies and runs unit tests.
3. Builds a Docker image.
4. Pushes the image to Docker Hub.
5. Applies Kubernetes Deployment and Service manifests to Minikube.
6. Verifies pods, deployment, service and rollout.

## Setup
- Change IMAGE_NAME in Jenkinsfile to your Docker Hub username/repository.
- Add Jenkins username/password credential ID `dockerhub-creds`; use a Docker Hub access token as the password.
- Jenkins execution environment needs Python 3, Docker, kubectl and access to the Minikube cluster.

## Run locally
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```
Open http://127.0.0.1:5000

## Important
For a fully automated pipeline, Jenkins, Docker, kubectl and Minikube must be reachable from the same Jenkins execution environment. The guide asks for Jenkins on AWS and deployment to Minikube, so avoid assuming a Minikube cluster on your Windows laptop is automatically accessible from EC2.

## Second run
After the first successful deployment, change `release="v1"` in app.py to `release="v2"`, commit and push, then run Jenkins again.

## Evidence
Capture GitHub files, Jenkins stage view and console output, Docker Hub tags, kubectl get pods/deployments/services, the running app, and the second deployment with v2.
