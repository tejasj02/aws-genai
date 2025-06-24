# GENAI Service with AWS

This service provides a lightweight, serverless text generation API using Groq’s LLMs, deployed via AWS Lambda.

Features
--------
- Groq-powered text generation (llama3-8b-8192)
- Basic content filtering
- CloudWatch logging and custom metrics
- REST API via API Gateway

API Endpoint
------------
POST /generate

URL: https://ax63u39z08.execute-api.us-east-1.amazonaws.com/generate
Content-Type: application/json

Request Body:
{
  "prompt": "Write a joke about robots."
}

Response:
{
  "response": "Sure! Why did the robot go to therapy? Because it had too many breakdowns."
}

Content Filtering
-----------------
Prompts containing any of the following blocked keywords are rejected:
["violence", "kill", "hate"]

Returns HTTP 403 with:
{
  "error": "Prompt violates content policy."
}

Monitoring
----------
- Logs available in CloudWatch under /aws/lambda/<function-name>
- Custom CloudWatch metric: TextGenService > Requests

Security
--------
- Groq API key is stored securely as a Lambda environment variable
- API access can be restricted via:
  - API Key (usage plan)
  - IAM roles or Lambda authorizer

Proof of Logs and Metrics

![image](https://github.com/user-attachments/assets/74123c38-1619-4152-9219-6cecaa0897a0)

![image](https://github.com/user-attachments/assets/c8b2e36b-6683-48a0-a361-a08695756548)

