# Flask API - Dockerized for Heroku

A REST API that returns the client's IP address and a simple addition, with CORS support and automated deployment using Docker and GitHub Actions to Heroku.

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

## Heroku Deployment

This application is configured to be deployed on Heroku. The `Procfile` file tells Heroku how to run the application using gunicorn as a web server.

## Docker Configuration

The project includes a `Dockerfile` that allows containerizing the application for deployment. The Docker image is configured to use the environment variables provided by Heroku.

## Automation with GitHub Actions

The CI/CD workflow is configured in `.github/workflows/heroku-deploy.yml`. This process automates:

1. Building the Docker image
2. Pushing the image to Heroku's container registry
3. Deploying the application on Heroku

### Setting up Secrets for GitHub Actions

For automatic deployment to work, you must configure the following secrets in your GitHub repository:

- `HEROKU_API_KEY`: Your Heroku API key
- `HEROKU_EMAIL`: The email address associated with your Heroku account
- `HEROKU_APP_NAME`: The name of your Heroku application

## Workflow

1. You push to the main branch (main/master) of your repository
2. GitHub Actions detects the push and executes the workflow
3. The Docker image is built with your application
4. The image is sent to the Heroku registry
5. The application is automatically deployed on Heroku
