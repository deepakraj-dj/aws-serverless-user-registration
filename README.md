### Serverless User Registration with JWT & CI/CD

## Overview
Fully serverless auth system with zero EC2 instances. Frontend served via S3 + CloudFront. Backend: Lambda functions behind API Gateway. DynamoDB stores user data. Passwords hashed with bcrypt, JWTs for stateless sessions. GitHub Actions automates deployment—separate pipelines for frontend/backend with path-based triggers.

## Architecture Diagram
![Architecture Diagram](docs/Architecture_diagram.png)

## How It All Works Together
1. User visits CloudFront-cached frontend (HTML form on S3)
2. Submits credentials to API Gateway /signup endpoint
3. Lambda function validates input → checks DynamoDB for existing user
4. Bcrypt hashes password → stores user in DynamoDB
5. Lambda generates JWT → sets httponly cookie (XSS-safe)
6. Frontend receives token → user logged in, redirected to dashboard
7. Subsequent requests include cookie → Lambda validates JWT

## Before You Start, Requirements:
- AWS Account (Lambda, API Gateway, DynamoDB, S3, CloudFront permissions)
- GitHub Account (for Actions secrets)
- Python 3.9+
- AWS CLI configured with credentials

Free Tier Note: DynamoDB read/write, Lambda invocations, API calls, and CloudFront transfers covered by AWS free tier. Monitor usage to avoid charges.
Get It Running (10 Minutes)
Step 1: Clone & Setup
bashgit clone https://github.com/yourusername/aws-serverless-user-registration.git
cd aws-serverless-user-registration
Step 2: Create AWS Resources
bash# Create DynamoDB table
aws dynamodb create-table \
  --table-name users \
  --attribute-definitions AttributeName=email,AttributeType=S \
  --key-schema AttributeName=email,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Create S3 bucket for frontend
aws s3 mb s3://your-unique-bucket-name

# Deploy Lambda function (package with bcrypt + jwt dependencies)
cd backend
pip install -r requirements.txt -t package/
cd package && zip -r ../lambda.zip . && cd ..
zip lambda.zip registerform_final.py
aws lambda create-function --function-name user-registration \
  --runtime python3.9 --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-exec \
  --handler registerform_final.lambda_handler --zip-file fileb://lambda.zip
Step 3: Connect API Gateway to Lambda
bash# Create API Gateway
aws apigateway create-rest-api --name registration-api
# (Use AWS Console to map POST /signup → Lambda)
Step 4: Setup GitHub Actions

Go to repo Settings → Secrets and variables → Actions
Add: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
Workflows auto-trigger on push to backend/ or frontend/ paths

Step 5: Test
bashcurl -X POST https://YOUR_API_GATEWAY_URL/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'
Security
✅ Bcrypt Hashing — Passwords never stored plain text (10 salt rounds)

✅ HTTPOnly Cookies — JWT set with httponly flag, prevents XSS/JavaScript access

✅ API Rate Limiting — API Gateway throttling (add 1000 req/sec limit)

✅ CORS Locked — API only accepts requests from CloudFront domain

✅ IAM Roles — Lambda has minimal permissions (DynamoDB, CloudWatch logs only)

✅ Secrets in GitHub — AWS credentials never in code (use GitHub Secrets)

⚠️ TODO: Add input validation (email format, password strength), implement login endpoint with JWT verification
What I Learned

Serverless Architecture: Eliminated server management—Lambda auto-scales, no cold servers, pay-per-execution model
Stateless Auth: JWT tokens enable horizontal scaling—no session storage needed
Security Best Practices: Bcrypt, httponly cookies, IAM least privilege access
CI/CD Automation: GitHub Actions trigger conditional deployments (path filters reduce unnecessary builds)
AWS Service Integration: Understood data flow across 6+ services (API Gateway → Lambda → DynamoDB)


## Architecture Diagram



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


# aws-serverless-user-registration
Serverless user registration on AWS using Lambda, API Gateway, DynamoDB, S3, CloudFront, and GitHub Actions CI/CD with JWT authentication.

## File Structure
```
.
├── .github/                      
│   └── workflows
│       ├── Backend.yml
│       └── Frontend.yml
├── backend/                  
|   └── registerform_final.py
├── docs/
│   └── Architecture_diagram.png
├── frontend
│   └── signup.html
├── LICENSE
├── README.md

```

