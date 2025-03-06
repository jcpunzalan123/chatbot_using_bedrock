import json
import boto3
import streamlit as st
from botocore.exceptions import ClientError


#bedrock client
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)
model_id  = "us.meta.llama3-1-8b-instruct-v1:0"

# Define the prompt for the model.
prompt = "What is the capital of Japan?"


def my_chatbot(prompt):
    # Embed the prompt in Llama 3's instruction format.
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    # Format the request payload using the model's native structure.
    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)
        # Decode the response body.
        model_response = json.loads(response["body"].read())
        return model_response

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    


st.title("Bedrock Chatbot")
freeform_text = st.text_area(label="what is your question?", max_chars=100)
if freeform_text:
    model_response = my_chatbot(freeform_text)
    st.write(model_response['generation'])
