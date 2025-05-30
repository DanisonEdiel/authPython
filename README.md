# Flask API - Dockerized for AWS EC2 via Docker Hub

A REST API that returns the client's IP address and a simple addition, with CORS support and automated deployment using Docker and GitHub Actions to AWS EC2 via Docker Hub.

## Installing Dependencies

```
pip install -r requirements.txt
```

## Running the Application Locally

```
python app.py
```

## Available Endpoints

- `GET /`: Home page, displays a message indicating that the API is functioning.
- `GET /api/hello`: Returns a JSON with the client's IP and a simple addition.

## Local Testing

You can test the API in the following ways:

1. **Web Browser**: Open http://localhost:5000/api/hello
2. **Postman**: Make a GET request to http://localhost:5000/api/hello
3. **Curl**: Run `curl http://localhost:5000/api/hello`

CORS support is enabled, so you can consume this API from any origin.

## Docker Configuration

The project includes a `Dockerfile` that allows containerizing the application for deployment. The Docker image is configured to use environment variables for flexibility.

## Deployment to AWS EC2 via Docker Hub

This application is configured to be deployed on an AWS EC2 instance using Docker Hub as intermediario. The workflow is as follows:

1. The application is built as a Docker image
2. The image is pushed to Docker Hub
3. The EC2 instance pulls the latest image from Docker Hub
4. The application is deployed as a Docker container on EC2

### Setting up Secrets for Deployment

For automatic deployment to work, you must configure the following secrets in your GitHub repository:

1. `DOCKERHUB_USERNAME`: Tu nombre de usuario de Docker Hub
2. `DOCKERHUB_TOKEN`: Tu token de acceso personal de Docker Hub
3. `EC2_HOST`: La dirección IP pública o DNS de tu instancia EC2
4. `EC2_USERNAME`: El nombre de usuario para conectarse a tu instancia EC2 (generalmente 'ec2-user' o 'ubuntu')
5. `EC2_SSH_KEY`: Tu clave SSH privada para conectarte a la instancia EC2

### Requisitos en la instancia EC2

Tu instancia EC2 debe tener:

1. Docker instalado
2. Puertos necesarios abiertos en el grupo de seguridad (80 para HTTP)

## Automation with GitHub Actions

### Docker Hub and EC2 Workflow

The CI/CD workflow is configured in `.github/workflows/dockerhub-push.yml`. This process automates:

1. Building the Docker image
2. Pushing the image to Docker Hub
3. Connecting to the EC2 instance via SSH
4. Pulling the latest image from Docker Hub
5. Deploying the application as a Docker container

## Workflow Execution

1. You push to the main branch (main/master) of your repository
2. GitHub Actions detects the push and executes the workflow
3. The Docker image is built with your application
4. The image is pushed to Docker Hub
5. The EC2 instance pulls the latest image and runs it

You can also manually trigger the deployment workflow from the Actions tab in GitHub.
