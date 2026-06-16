# Serverless User Registration with JWT & CI/CD

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

## How to Deploy

### Step 1: Clone & Setup
```bash
git clone https://github.com/deepakraj-dj/aws-serverless-user-registration.git
cd aws-serverless-user-registration
```
### Step 2: Create DynamoDB Table (Console)
- Go to AWS Console → DynamoDB → Create Table
- Table name: users
- Partition key: email (String)
- Billing mode: Pay-per-request
- Click Create

### Step 3: Create S3 Bucket (Console)
- Go to S3 → Create Bucket
- Name: your-unique-bucket-name-registration
- Block public access: Uncheck "Block all public access"
- Upload frontend/signup.html to bucket
- Go to Bucket Properties → Static website hosting → Enable
- Set index document: signup.html

### Step 4: Create CloudFront Distribution (Console)
- Go to CloudFront → Create Distribution
- Origin domain: Select your S3 bucket
- Viewer protocol: Redirect HTTP to HTTPS
- Cache policy: CachingOptimized
- Click Create
- Copy CloudFront domain (e.g., d123xyz.cloudfront.net)

### Step 5: Create Lambda Function (Console)
- Go to Lambda → Create Function
- Function name: user-registration
- Runtime: Python 3.9
- Execution role: Create new role with DynamoDB access
- Paste code from backend/registerform_final.py into editor
- Add layer for dependencies:
  - Create ZIP with bcrypt and PyJWT libraries 
  - Go to Layers → Create layer → Upload ZIP
  - Attach layer to your function

### Step 6: Create API Gateway (Console)

- Go to API Gateway → Create API → REST API
- Name: registration-api
- Create resource: /signup
- Create POST method → Lambda integration → Select user-registration
- Enable CORS:
  - Right-click /signup → Enable CORS
  - Access-Control-Allow-Origin: https://d123xyz.cloudfront.net (your CloudFront domain)
- Deploy API → Stage name: prod
- Copy API invoke URL (e.g., https://abc123.execute-api.us-east-1.amazonaws.com/prod)

### Step 7: Update Frontend (in S3)
- Edit signup.html → Change API endpoint:
- javascript// In your HTML/JS, update:
- const API_URL = 'https://abc123.execute-api.us-east-1.amazonaws.com/prod/signup';
- Upload updated signup.html back to S3 bucket.

### Step 8: Setup GitHub Actions (Console)
- Go to your GitHub repo → Settings → Secrets and variables → Actions
- Click "New repository secret" → Add:
    - AWS_ACCESS_KEY_ID (from your AWS IAM user)
    - AWS_SECRET_ACCESS_KEY (from your AWS IAM user)
    - AWS_REGION (e.g., us-east-1)
    - S3_BUCKET (your bucket name)
    - LAMBDA_FUNCTION_NAME (user-registration)
      
- Workflows will auto-trigger on push

### Step 9: Test
```bash
curl -X POST https://abc123.execute-api.us-east-1.amazonaws.com/prod/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'
```
Or visit https://d123xyz.cloudfront.net and submit the form.

## Demo / Results

### 1. Frontend - Signup Form (S3 + CloudFront)
![Frontend](Frontend.png)
URL: d1su39mqqdhlc7.cloudfront.net

### 2. CI/CD Pipeline - Frontend Deployment
[Image 1 - "Deploy to S3 and CloudFront" pipeline]
- Checkout code
- Copy files to S3
- Invalidate CloudFront cache
- Completed in 6 seconds

### 3. Backend Deployment & Registration Success
[Image from first screenshot - Lambda deployment]
Shows successful user registration with JWT cookie creation

### 4. User Registration Response
[The alert/response screenshot with "Cookie created successfully"]

## Security
✅ Bcrypt Hashing — Passwords never stored plain text (10 salt rounds)

✅ HTTPOnly Cookies — JWT set with httponly flag, prevents XSS/JavaScript access

✅ API Rate Limiting — API Gateway throttling (add 1000 req/sec limit)

✅ CORS Locked — API only accepts requests from CloudFront domain

✅ IAM Roles — Lambda has minimal permissions (DynamoDB, CloudWatch logs only)

✅ Secrets in GitHub — AWS credentials never in code (use GitHub Secrets)

## What I Learned

- Serverless Architecture: Eliminated server management—Lambda auto-scales, no cold servers, pay-per-execution model
- Stateless Auth: JWT tokens enable horizontal scaling—no session storage needed
- Security Best Practices: Bcrypt, httponly cookies, IAM least privilege access
- CI/CD Automation: GitHub Actions trigger conditional deployments (path filters reduce unnecessary builds)
- AWS Service Integration: Understood data flow across 6+ services (API Gateway → Lambda → DynamoDB)

## File Structure
```
.
├── .github/                      
│   └── workflows
│       ├── Backend.yml               # CI/CD: Auto-deploy Lambda on code push
│       └── Frontend.yml              # CI/CD: Auto-deploy to S3 & invalidate CloudFront
├── backend/                  
|   └── registerform_final.py         # Lambda handler: User registration with JWT auth
├── docs/
│   └── Architecture_diagram.png      # Full system architecture flo
├── frontend
│   └── signup.html                   # HTML form: User registration UI
├── LICENSE
├── README.md                         # Project documentation & setup guide


