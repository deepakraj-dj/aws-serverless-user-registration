
# Serverless Registration System with JWT and CI/CD

## Overview

This project is a fully serverless login and registration system — no EC2, no servers 
to manage. The goal was to build a secure auth flow entirely on managed AWS services 
and automate deployment end-to-end with CI/CD.

The frontend is a static site delivered via S3 + CloudFront. The backend is a set of 
Lambda functions sitting behind API Gateway, handling registration and login requests. 
User data is stored in DynamoDB.

Passwords are hashed with bcrypt before storage — plain text never touches the database. 
Sessions are managed with JWTs so the backend stays completely stateless.
The JWT are generated and created into an httponly cookie in the backend and sends to user to avoid javascript and XSS.

Deployment is automated via GitHub Actions with separate pipelines for frontend and 
backend. Path-specific triggers mean a CSS change won't kick off a Lambda deployment. 
AWS credentials are stored as GitHub Secrets.


## Architecture

![Architecture Diagram](docs/Architecture_diagram.png)

## Tech Stack

- AWS Cloudfront
- S3
- API Gateway
- AWS Lambda (Python)
- DynamoDB
- JWT
- Bcrypt
- CI/CD
- Github Actions
- Github Secrets

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /signup | Creates new user and return token |


## How to Deploy


## Security Considerations

=======
# aws-serverless-user-registration
Serverless user registration on AWS using Lambda, API Gateway, DynamoDB, S3, CloudFront, and GitHub Actions CI/CD with JWT authentication.
>>>>>>> 5967d04227a95f16fcae69bd058e6e31358d4655
