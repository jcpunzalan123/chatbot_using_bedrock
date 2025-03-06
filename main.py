import os
import boto3
import streamlit as st

from langchain.chains import LLMChain
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate

#bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)
modelID = "meta.llama3-1-8b-instruct-v1:0"

llm = ChatBedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 1000,"temperature":0.9}
)

def my_chatbot(prompt):
    # prompt = PromptTemplate(
    #     input_variables=["language", "freeform_text"],
    #     template="You are a chatbot. You are in {language}.\n\n{freeform_text}"
    # )

    # bedrock_chain = LLMChain(llm=llm, prompt=prompt)


    # response=bedrock_chain({'language':language, 'freeform_text':freeform_text})
    response = llm.invoke(prompt)
    return response

st.title("Bedrock Chatbot")

response = my_chatbot("What is the capital of Japan?")
print(response)