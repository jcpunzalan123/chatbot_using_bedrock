import json
import boto3


client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)
model_id  = "us.meta.llama3-1-8b-instruct-v1:0"


def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    body = json.loads(event['body'])
    prompt = body.get('prompt', "Hello! How can I help you today?")    

    # Embed the prompt in Llama 3's instruction format.
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    # Format the request payload using the model's native structure.
    body = {
        "prompt": formatted_prompt,
        "max_gen_len": 200,
        "temperature": 0.0,
    }

    # Convert the native request to JSON.
    request = json.dumps(body)

    response = client.invoke_model(modelId=model_id, body=request)
    # Decode the response body.
    model_response = json.loads(response["body"].read())['generation']

    api_response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({
            'prompt':prompt,
            'response':model_response
        })
    }

    return api_response
