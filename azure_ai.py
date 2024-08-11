# Import built-in libraries
from dotenv import load_dotenv
import os
import time
import requests
# Import libraries for Azure OpenAI
from openai import AzureOpenAI
# Load environment variables
from prompt import GetPrompt

class AzureOpenAIClient:
    def __init__(self):
        load_dotenv()
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.api_version = os.getenv('API_VERSION')
        self.assistant_id = os.getenv('ASSISTANT_ID')
        self.thread_id = os.getenv('THREAD_ID')
        self.model = os.getenv('MODEL')

        self.message_api = f"{self.azure_endpoint}openai/threads/{self.thread_id}/messages"
        self.run_api = f"{self.azure_endpoint}openai/threads/{self.thread_id}/runs"

        self.params = {
            "api-version": self.api_version
        }

        self.headers = {
            "api-key": self.api_key
        }

    def add_messages(self, messages='hello'):
        body = {
            "role": "user",
            "content": messages
        }
        response = requests.post(self.message_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def runs_thread(self):
        body = {
            "assistant_id": self.assistant_id,
            "model": self.model
        }

        response = requests.post(self.run_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def get_chat_history(self):
        response = requests.get(self.message_api, params=self.params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data["data"][0]["role"] != 'assistant':
                time.sleep(1)
                return self.get_chat_history()
            else:
                return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def request_match(self, vendor_data, bzbs_data):
        prompt = GetPrompt(vendor_data, bzbs_data).prompt
        self.add_messages(messages=prompt)
        self.runs_thread()
        result = self.get_chat_history()["data"][0]["content"][0]['text']['value']
        return result
