import os
from dotenv import load_dotenv
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ['AZURE_ENDPOINT'],
    api_key=os.environ['AZURE_OPENAI_API_KEY'],
    api_version=os.environ['AZURE_API_VERSION']
)

def getLLMResponse(promptMessage):
      response = client.chat.completions.create(
        model=os.environ['AZURE_OPENAI_CHAT_MODEL'],
        messages= promptMessage,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    
      return response.choices[0].message.content