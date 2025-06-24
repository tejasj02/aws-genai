import os
import json
import requests
import logging
import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CloudWatch client
cloudwatch = boto3.client('cloudwatch')

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
    except:
        body = event

    prompt = body.get("prompt", "").strip()
    logger.info(f"Received prompt: {prompt}")

    if not prompt:
        logger.warning("Prompt missing.")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Prompt missing"})
        }

    blocked_keywords = ["violence", "kill", "hate"]
    if any(word in prompt.lower() for word in blocked_keywords):
        logger.warning("Prompt blocked due to content policy.")
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Prompt violates content policy."})
        }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        logger.info(f"Generated response: {content}")

        # Custom metric
        cloudwatch.put_metric_data(
            Namespace='TextGenService',
            MetricData=[{
                'MetricName': 'Requests',
                'Unit': 'Count',
                'Value': 1
            }]
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"response": content})
        }

    except Exception as e:
        logger.error(f"Error during text generation: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
