import os
from dotenv import load_dotenv
import openai

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
DEPLOYMENT_EMBEDDINGS = os.getenv('AZURE_DEPLOYMENT_NAME_EMBEDDINGS')
DEPLOYMENT_CHAT = os.getenv('AZURE_DEPLOYMENT_NAME_CHAT')

openai.api_type = 'azure'
openai.api_key = OPENAI_KEY
openai.api_base = OPENAI_ENDPOINT
openai.api_version = '2023-05-15'

class AzureEmbedding:
    def get_embedding(self, text: str):
        response = openai.Embedding.create(
            input=text,
            engine=DEPLOYMENT_EMBEDDINGS
        )
        return response['data'][0]['embedding']

class AzureChatGPT:
    def chat(self, messages):
        response = openai.ChatCompletion.create(
            deployment_id=DEPLOYMENT_CHAT,
            messages=messages,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
