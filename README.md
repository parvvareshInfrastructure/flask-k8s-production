# Flask with Kubernetes

A simple Flask application containerized with Docker and deployed to Kubernetes.

## Overview

This project demonstrates how to build, containerize, and deploy a Flask web application to a Kubernetes cluster. The application serves a simple "Hello from Flask on Kubernetes!" message.

## Project Structure

```
flask-with-kubernetes/
├── app/
│   ├── app.py              # Flask application code
│   └── requirements.txt    # Python dependencies
├── Dockerfile              # Docker image configuration
├── k8s.yaml               # Kubernetes deployment and service manifests
└── README.md              # This file
```

## Prerequisites

- Docker
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool

## Building the Docker Image

Build the Docker image with the following command:

```bash
docker build -t flask-demo:1.0 .
```

## Running Locally with Docker

Run the application in a Docker container:

```bash
docker run -p 5000:5000 flask-demo:1.0
```

Access the application at: `http://localhost:5000`

## Deploying to Kubernetes

### Step 1: Create Namespace

```bash
kubectl create namespace demo
```

### Step 2: Apply Kubernetes Manifests

```bash
kubectl apply -f k8s.yaml
```

### Step 3: Verify Deployment

Check if pods are running:

```bash
kubectl get pods -n demo
```

Check service status:

```bash
kubectl get svc -n demo
```

## Accessing the Application in Kubernetes

### Option 1: Port Forward

```bash
kubectl port-forward -n demo service/flask-svc 8080:80
```

Then visit: `http://localhost:8080`

### Option 2: Using Minikube Service (if using minikube)

```bash
minikube service flask-svc -n demo
```

## Kubernetes Configuration

The application is deployed with the following configuration:

- **Deployment**: 3 replicas for high availability
- **Service Type**: ClusterIP (internal access only)
- **Container Port**: 5000
- **Service Port**: 80 (maps to container port 5000)
- **Image Pull Policy**: IfNotPresent

## Scaling the Application

Scale the deployment to a different number of replicas:

```bash
kubectl scale deployment flask-app -n demo --replicas=5
```

## Viewing Logs

View logs from a specific pod:

```bash
kubectl logs -n demo <pod-name>
```

View logs from all pods with the app label:

```bash
kubectl logs -n demo -l app=flask-app
```

## Cleaning Up

Remove all resources:

```bash
kubectl delete -f k8s.yaml
kubectl delete namespace demo
```

## Application Details

- **Framework**: Flask 3.0.2
- **WSGI Server**: Gunicorn 21.2.0
- **Python Version**: 3.11
- **Base Image**: python:3.11-slim

## Development

To modify the application:

1. Edit the Flask code in `app/app.py`
2. Rebuild the Docker image
3. If using Kubernetes, update the image tag in `k8s.yaml`
4. Reapply the Kubernetes manifests

## License

This project is open source and available under the MIT License.