# Product Name Matching with OCR and Azure OpenAI

This project automates the matching of product names between vendor's products listed on invoice images and the products in my company database. The solution leverages an OCR API for text extraction from images and Azure OpenAI for intelligent processing and matching.

## Table of Contents
- [Workflow](#workflow)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Workflow
The following steps outline the workflow of the project:

1. **Invoice Image Processing**:
   - The system reads invoice images stored in Azure Blob Storage.
   - It forwards the Blob URL to an OCR API to extract the raw text content from the images.

2. **Raw Content Formatting**:
   - The extracted raw content is passed to the first AI Agent.
   - The AI Agent formats the raw product data into a structured CSV format.

3. **Product Matching**:
   - The system reads the product data from Buzzebees' database.
   - Both the formatted invoice data and the Buzzebees product data are sent to a second AI Agent.
   - The second AI Agent compares the two datasets, finds the most similar products, and returns the matching results as a CSV file.

## Features
- **OCR Integration**: Automatically extract text from invoice images using an OCR API.
- **AI-Powered Formatting**: Use Azure OpenAI to convert unstructured raw text into a structured CSV format.
- **Product Matching**: Leverage AI to match vendor products with Buzzebees' product catalog.

## Installation
To set up and run this project, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/pladee42/AI-Product-Mapping.git
   cd product-matching
   ```
2. **Install Dependencies**:

  ```bash
   pip install -r requirements.txt
   ```
3. **Configure Azure Services**:
  •	Set up Azure Blob Storage and upload the file in your Blob.
	•	Configure the OCR API endpoint and key.
	•	Set up Azure OpenAI and configure the API keys and endpoint.
4. **Set Environment Variables**:
  Create a .env file per the format below:

  ```bash
  AZURE_OPENAI_ENDPOINT=openai_api_endpoint
  AZURE_OPENAI_API_KEY=openai_api_key
  API_VERSION=openai_api_version
  PRODUCT_MATCHING_AGENT_ID=your_product_matching_agentid
  PRODUCT_EXTRACTOR_AGENT_ID=your_product_formatter_agentid
  MODEL=your_ai_model
  BZBS_ENDPOINT=your_ocr_api_endpoint
  BZBS_BLOB_URL=your_azure_blob_endpoint
  ```

## Usage
Follow these steps to use the project:

1. **Upload Invoice Images**:
   - Place the invoice images into the designated Azure Blob Storage container.

2. **Run the Matching Script**:
   - Execute the main script to start the process:

   ```bash
   python main.py
   ```

3. **Check Results**:
   - After processing, the matched results will be saved as a CSV file in the output directory.
  
