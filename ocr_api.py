import requests
from dotenv import load_dotenv
import os

class BZBSClient:
    def __init__(self):
        # Load environment variables, allowing overrides if needed
        load_dotenv(override=True)
        
        # Set up the API endpoint and blob URL from environment variables
        self.bzbs_endpoint = os.getenv('BZBS_ENDPOINT')
        self.bzbs_blob = os.getenv('BZBS_BLOB_URL')
        
        # Define the full URLs for the APIs
        self.add_api = f"{self.bzbs_endpoint}demo/add"
        self.detail_api = f"{self.bzbs_endpoint}demo/detail"

    def add_file(self, file_name):
        """
        Adds a file to the system by sending its URL to the 'add' API.
        
        Args:
            file_name (str): The name of the file to be added.
        
        Returns:
            str: The document reference ID if successful, otherwise an error message.
        """
        # Construct the request body with the file URL
        body = {
            "FileUrl": f"{self.bzbs_blob}{file_name}"
        }

        # Send a POST request to the add API
        response = requests.post(self.add_api, json=body)

        # Handle the response
        if response.status_code == 200:
            # Parse the JSON response and extract the document reference ID
            data = response.json()
            file_id = data["Data"]["DocumentReferenceId"]
            return file_id
        else:
            # Print the error status and return the response text
            print(f"Request failed with status code {response.status_code}")
            return response.text

    def get_file_detail(self, file_id):
        """
        Retrieves the details of a file using its document reference ID.
        
        Args:
            file_id (str): The document reference ID of the file.
        
        Returns:
            dict: The content of the file if successful, otherwise an error message.
        """
        # Set up the query parameters with the file ID
        params = {
            "DocumentReferenceId": file_id
        }

        # Send a GET request to the detail API
        response = requests.get(self.detail_api, params=params)

        # Handle the response
        if response.status_code == 200:
            # Parse the JSON response and extract the file content
            data = response.json()
            content = data["Data"]["Content"]
            return content
        else:
            # Print the error status and return the response text
            print(f"Request failed with status code {response.status_code}")
            return response.text
