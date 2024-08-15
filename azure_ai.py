# Import necessary libraries
from dotenv import load_dotenv
import os
import time
import requests
import json
# Import custom module for generating prompts
from prompt import GetPrompt

class AzureOpenAIClient:
    def __init__(self, assistant_id=None):
        """
        Initializes the AzureOpenAIClient with environment variables.
        """
        load_dotenv(override=True)  # Load environment variables from a .env file
        
        # Set up Azure OpenAI API details
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.api_version = os.getenv('API_VERSION')
        self.assistant_id = assistant_id
        self.model = os.getenv('MODEL')

        # Set up request parameters and headers
        self.params = {
            "api-version": self.api_version
        }

        self.headers = {
            "api-key": self.api_key
        }

    def new_thread(self):
        print("=== Creating Open AI Thread ===")
        thread_api = self.azure_endpoint + "openai/threads"
        response = requests.post(thread_api, params=self.params, headers=self.headers)
        print(f"=== Thread Created at {response.json()['id']}===")
        return response.json()['id']

    def add_messages(self, messages : str, thread_id : str):
        """
        Sends a message to the Azure OpenAI API.
        
        Args:
            messages (str): The message content to be sent.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        print("=== Processing Open AI Messages API ===")
        message_api = self.azure_endpoint + "openai/threads/" + thread_id + "/messages"

        body = {
            "role": "user",
            "content": messages
        }
        response = requests.post(message_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            return response.json()  # Return the parsed JSON response
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def runs_thread(self, thread_id : str, assistant_id : str):
        """
        Initiates a run in the Azure OpenAI thread.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        print("=== Processing Open AI Run Thread API ===")
        run_api = self.azure_endpoint + "openai/threads/" + thread_id + "/runs"
        body = {
            "assistant_id": assistant_id,
            "model": self.model
        }

        response = requests.post(run_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            return response.json()  # Return the parsed JSON response
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def get_chat_history(self, thread_id : str):
        """
        Retrieves the chat history from the Azure OpenAI API.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        print("=== Processing Open AI Chat History API ===")
        message_api = self.azure_endpoint + "openai/threads/" + thread_id + "/messages"
        response = requests.get(message_api, params=self.params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if (data["data"][0]["role"] != 'assistant') or  (len(data["data"][0]["content"]) == 0) :
                time.sleep(5)  # Wait for a second if the assistant hasn't responded yet
                return self.get_chat_history(thread_id=thread_id)  # Recursively call until an assistant response is found
            else:
                return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text
        
    def extract_json(self, response : str):
        """
        Extracts JSON data from a response string.
        
        Args:
            response (str): The response string containing JSON data.
        
        Returns:
            dict: Parsed JSON data.
        """
        print("=== Processing JSON Extraction ===")
        result = json.loads(response.split('```')[1].replace('\n', '').replace('json', ''))
        with open("output/result.json" , "w", encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result
