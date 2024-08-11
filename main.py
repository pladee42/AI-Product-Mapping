from azure_ai import AzureOpenAIClient
from ocr_api import BZBSClient
import pandas as pd

bzbs_client = BZBSClient()
azure_client = AzureOpenAIClient()


vendor_file_name = input("Please input vendor file name: ")
bzbs_file_name = input("Please input Buzzebees file name: ")

file_id = bzbs_client.add_file(file_name=vendor_file_name)
vendor_data = bzbs_client.get_file_detail(file_id=file_id)

with open(f"input/{bzbs_file_name}","r") as f:
    bzbs_data = f.read()

result = azure_client.request_match(vendor_data=vendor_data, bzbs_data=bzbs_data)

df = pd.DataFrame(result)
df.to_csv(f"output/{bzbs_file_name}_result.csv", index=False)