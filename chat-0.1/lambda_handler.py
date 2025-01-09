import json
from app import reverse_text

def lambda_handler(event, context):
    body = json.loads(event["body"])
    input_text = body["input_text"]
    result = reverse_text(input_text)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"result": result})
    }
