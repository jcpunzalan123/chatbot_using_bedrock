import os
import boto3
import streamlit as st

from langchain.chains import LLMChain
from langchain_community.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate

print(os.environ)