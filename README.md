# Flask with Kubernetes

A simple Flask application demonstrating Kubernetes deployment with ConfigMaps, Secrets, Services, Ingress, and Horizontal Pod Autoscaling (HPA).

## Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI pipeline (test & lint)
│       ├── docker-build.yml # Docker build and push
│       ├── deploy.yml      # Kubernetes deployment
│       └── pr-checks.yml   # Pull request validations
├── app/
│   ├── app.py              # Flask application
│   ├── test_app.py         # Unit tests
│   └── requirements.txt    # Python dependencies
├── k8s/
│   ├── namespace.yaml      # Kubernetes namespace
│   ├── configmap.yaml      # Application configuration
│   ├── secret.yaml         # Sensitive data
│   ├── deployment.yaml     # Application deployment
│   ├── service.yaml        # Internal service
│   ├── ingress.yaml        # External routing
│   └── hpa.yaml           # Horizontal Pod Autoscaler
├── Dockerfile              # Container image definition
└── README.md              # This file
```

## Application Features

The Flask application exposes three endpoints:

- `GET /` - Returns a greeting message with the application version
- `GET /health` - Health check endpoint (JSON response)
- `GET /secret` - Returns the API key from environment variables

### Environment Variables

- `APP_MESSAGE` - Custom message (default: "Hello (default)")
- `APP_VERSION` - Application version (default: "dev")
- `API_KEY` - API authentication key (default: "no-key")

## Prerequisites

- Docker
- Kubernetes cluster (minikube, kind, or any K8s cluster)
- kubectl configured to access your cluster

## Quick Start

### 1. Build Docker Image

```bash
docker build -t flask-k8s-demo:1.0 .
```

### 2. Deploy to Kubernetes

Apply all Kubernetes resources in order:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secret
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Enable autoscaling (optional)
kubectl apply -f k8s/hpa.yaml
```

Or apply all at once:

```bash
kubectl apply -f k8s/
```

### 3. Verify Deployment

```bash
# Check pods
kubectl get pods -n demo

# Check service
kubectl get svc -n demo

# Check ingress
kubectl get ingress -n demo
```

### 4. Access the Application

#### Option 1: Port Forward

```bash
kubectl port-forward -n demo svc/flask-svc 8080:80
curl http://localhost:8080/
```

#### Option 2: Ingress (requires Ingress Controller)

Add to `/etc/hosts`:
```
127.0.0.1 flask.local
```

If using minikube:
```bash
minikube tunnel
```

Then access:
```bash
curl http://flask.local/
curl http://flask.local/health
curl http://flask.local/secret
```

## Kubernetes Resources

### Deployment
- **Replicas**: 3 (initial)
- **Image**: flask-k8s-demo:1.0
- **Health Checks**: Readiness and liveness probes on `/health`
- **Configuration**: Uses ConfigMap and Secret for environment variables

### Service
- **Type**: ClusterIP
- **Port**: 80 → 5000

### Ingress
- **Host**: flask.local
- **Path**: / (all paths)

### HPA (Horizontal Pod Autoscaler)
- **Min Replicas**: 2
- **Max Replicas**: 6
- **Metric**: CPU utilization (target: 50%)

### ConfigMap
- `APP_MESSAGE`: "Hello from ConfigMap!\n"
- `APP_VERSION`: "1.0"

### Secret
- `API_KEY`: "super-secret-key" (stored as Secret)

## Development

### Run Locally

```bash
cd app
pip install -r requirements.txt
python app.py
```

Access at `http://localhost:5000`

### Run Tests

```bash
cd app
pip install pytest pytest-cov
pytest test_app.py
```

With coverage:
```bash
pytest --cov=. --cov-report=html test_app.py
```

### Update Configuration

To update the application message:
```bash
kubectl edit configmap flask-config -n demo
kubectl rollout restart deployment/flask-app -n demo
```

To update the secret:
```bash
kubectl edit secret flask-secret -n demo
kubectl rollout restart deployment/flask-app -n demo
```

## CI/CD with GitHub Actions

This project includes automated CI/CD workflows using GitHub Actions:

### Workflows

#### 1. CI - Test and Lint (`.github/workflows/ci.yml`)
Runs on every push and pull request to `main` and `develop` branches.

- **Linting**: Runs flake8 to check code quality
- **Testing**: Executes pytest with coverage reporting
- **Security**: Scans code for vulnerabilities using Trivy
- **Coverage**: Uploads coverage reports to Codecov

#### 2. Docker Build and Push (`.github/workflows/docker-build.yml`)
Builds and pushes Docker images to GitHub Container Registry.

- **Triggers**: 
  - Push to `main` branch
  - Git tags matching `v*.*.*`
  - Pull requests (build only, no push)
- **Features**:
  - Multi-platform build support
  - Automatic tagging (latest, version, SHA)
  - Image caching for faster builds
  - Security scanning with Trivy

#### 3. Deploy to Kubernetes (`.github/workflows/deploy.yml`)
Manual deployment workflow triggered via GitHub UI.

- **Manual trigger** with environment selection (dev/staging/production)
- Configurable image tag
- Automated rollout with health checks
- Smoke tests after deployment

#### 4. PR Checks (`.github/workflows/pr-checks.yml`)
Additional checks for pull requests.

- **Kubernetes validation**: Validates all K8s manifests
- **Dockerfile linting**: Runs Hadolint
- **Dependency checks**: Scans for security vulnerabilities

### Setup Requirements

To use the CI/CD pipelines, configure the following:

1. **GitHub Container Registry** (automatic with GitHub token)
   ```bash
   # Images are pushed to: ghcr.io/<username>/<repository>
   ```

2. **Kubernetes Deployment** (optional, for deploy workflow)
   - Add `KUBECONFIG` secret in repository settings
   - Set up GitHub Environments (dev, staging, production)

3. **Codecov** (optional, for coverage reports)
   - Sign up at https://codecov.io
   - No additional secrets needed with GitHub Actions

### Using the Workflows

#### Automated CI on Push
```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

#### Manual Deployment
1. Go to Actions tab in GitHub
2. Select "Deploy to Kubernetes"
3. Click "Run workflow"
4. Choose environment and image tag
5. Click "Run workflow"

#### Release with Docker Build
```bash
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Build Docker image
- Tag as `v1.0.0`, `1.0`, `1`, and `latest`
- Push to GitHub Container Registry

### Using Published Images

Update [k8s/deployment.yaml](k8s/deployment.yaml) to use the published image:

```yaml
containers:
  - name: flask
    image: ghcr.io/<username>/<repository>:latest
```

## Monitoring

View application logs:
```bash
kubectl logs -n demo -l app=flask-app -f
```

Check HPA status:
```bash
kubectl get hpa -n demo
kubectl describe hpa flask-hpa -n demo
```

## Cleanup

Remove all resources:
```bash
kubectl delete namespace demo
```

Or remove individually:
```bash
kubectl delete -f k8s/
```

