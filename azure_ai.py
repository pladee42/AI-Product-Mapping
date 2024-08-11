# Import necessary libraries
from dotenv import load_dotenv
import os
import time
import requests
import json
# Import custom module for generating prompts
from prompt import GetPrompt

class AzureOpenAIClient:
    def __init__(self):
        """
        Initializes the AzureOpenAIClient with environment variables.
        """
        load_dotenv(override=True)  # Load environment variables from a .env file
        
        # Set up Azure OpenAI API details
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.api_version = os.getenv('API_VERSION')
        self.assistant_id = os.getenv('ASSISTANT_ID')
        self.thread_id = os.getenv('THREAD_ID')
        self.model = os.getenv('MODEL')

        # Define the API endpoints
        self.message_api = f"{self.azure_endpoint}openai/threads/{self.thread_id}/messages"
        self.run_api = f"{self.azure_endpoint}openai/threads/{self.thread_id}/runs"

        # Set up request parameters and headers
        self.params = {
            "api-version": self.api_version
        }

        self.headers = {
            "api-key": self.api_key
        }

    def add_messages(self, messages='hello'):
        """
        Sends a message to the Azure OpenAI API.
        
        Args:
            messages (str): The message content to be sent.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        body = {
            "role": "user",
            "content": messages
        }
        response = requests.post(self.message_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            return response.json()  # Return the parsed JSON response
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def runs_thread(self):
        """
        Initiates a run in the Azure OpenAI thread.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        body = {
            "assistant_id": self.assistant_id,
            "model": self.model
        }

        response = requests.post(self.run_api, params=self.params, headers=self.headers, json=body)

        if response.status_code == 200:
            return response.json()  # Return the parsed JSON response
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def get_chat_history(self):
        """
        Retrieves the chat history from the Azure OpenAI API.
        
        Returns:
            dict or str: JSON response if successful, error text otherwise.
        """
        response = requests.get(self.message_api, params=self.params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data["data"][0]["role"] != 'assistant':
                time.sleep(1)  # Wait for a second if the assistant hasn't responded yet
                return self.get_chat_history()  # Recursively call until an assistant response is found
            else:
                return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return response.text
        
    def extract_json(self, response):
        """
        Extracts JSON data from a response string.
        
        Args:
            response (str): The response string containing JSON data.
        
        Returns:
            dict: Parsed JSON data.
        """
        return json.loads(response.split('```')[1].replace('\n', '').replace('json', ''))

    def request_match(self, vendor_data, bzbs_data):
        """
        Sends a request to match vendor and bzbs data using Azure OpenAI API.
        
        Args:
            vendor_data (str): Vendor data to be matched.
            bzbs_data (str): Bzbs data to be matched.
        
        Returns:
            dict: The result of the matched data.
        """
        # Generate a prompt using the provided data
        prompt = GetPrompt(vendor_data, bzbs_data).prompt
        # Send the generated prompt as a message to the API
        self.add_messages(messages=prompt)
        # Run the thread to process the request
        self.runs_thread()
        # Get the assistant's response
        response = self.get_chat_history()["data"][0]["content"][0]['text']['value']
        # Extract JSON data from the response
        result = self.extract_json(response)
        return result
