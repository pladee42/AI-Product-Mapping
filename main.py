from azure_ai import AzureOpenAIClient
from ocr_api import BZBSClient
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Import custom module for generating prompts
from prompt import GetPrompt

start = time.perf_counter()
load_dotenv(override=True)
extractor_agent_id = os.getenv('PRODUCT_EXTRACTOR_AGENT_ID')
matching_agent_id = os.getenv('PRODUCT_MATCHING_AGENT_ID')


bzbs_client = BZBSClient()
product_extractor_agent = AzureOpenAIClient(assistant_id=extractor_agent_id)
product_matching_agent = AzureOpenAIClient(assistant_id=matching_agent_id)

def write_log(filename, data):
    with open(f"log/{filename}.txt","w",encoding='utf-8') as f:
        f.write(data)

def agent_chat(agent, messages):
    thread_id = agent.new_thread()
    agent.add_messages(thread_id=thread_id, messages=messages)
    agent.runs_thread(thread_id=thread_id, assistant_id=agent.assistant_id)

    if agent.assistant_id == matching_agent_id:
        response  = agent.get_chat_history(thread_id=thread_id)["data"][0]["content"][0]['text']['value']
        write_log(filename="result", data=response)
        return agent.extract_json(response)
    else:
        return agent.get_chat_history(thread_id=thread_id)["data"][0]["content"][0]['text']['value']
    


vendor_file_name = input("Please input vendor file name: ")
bzbs_file_name = input("Please input Buzzebees file name: ")

file_id = bzbs_client.add_file(file_name=vendor_file_name)
ocr_data = bzbs_client.get_file_detail(file_id=file_id)
vendor_data = agent_chat(agent=product_extractor_agent, messages=ocr_data)
write_log(filename="vendor", data=vendor_data)

print(f"1st Agent Time taken: {time.perf_counter() - start} seconds")

with open(f"input/bzbs/{bzbs_file_name}","r",encoding='utf-8') as f:
    bzbs_data = f.read()

prompt = GetPrompt(vendor_data, bzbs_data).prompt
write_log(filename="prompt", data=prompt)

result = agent_chat(agent=product_matching_agent, messages=prompt)

df = pd.DataFrame(result)
df.to_csv(f"output/{bzbs_file_name.replace('.csv','')}_result3.csv", index=False, encoding='utf-8')
print(f"Total Time taken: {time.perf_counter() - start} seconds")
