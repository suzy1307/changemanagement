import requests
import json
import time

url = "https://chat-ms-amaiz-backend-ms-prod.at-azure-amaiz-55185456.corp.amdocs.azr/api/v1/chats/send-message"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
data = {
  "username": "shwetac",  # Your username
  "apikey": "01923c96-48f8-4fd4-9aae-651e3bee9586",  # Your API key
  "conv_id": "",
  "messages": [
    {
      "user": "hi wats up?"
    }
  ],
  "promptfilename": "",
  "promptname": "",
  "prompttype": "system",
  "promptrole": "act as ChatGPT",
  "prompttask": "",
  "promptexamples": "",
  "promptformat": "",
  "promptrestrictions": "",
  "promptadditional": "",
  "max_tokens": 4000,
  "model_type": "GPT3.5_16K",
  "temperature": 0.1,
  "topKChunks": 2,
  "read_from_your_data": False,
  "document_groupname": "",
  "document_grouptags": [],
  "data_filenames": [],
  "find_the_best_response": False,
  "chat_attr": {},
  "additional_attr": {}
}

ca_bundle_path = 'C:/Users/shwetac/project/changemanagement/certs/amdcerts.pem'

# Send a Post Request to send-message endpoint
response = requests.post(url, headers=headers, data=json.dumps(data), verify=ca_bundle_path)

# Get Task ID from response
task_id = response.json().get("task_id")
if not task_id:
    print("Error: No task_id in response")
    exit()

# Get status of task by using task_id from status endpoint
status_url = f"https://chat-ms-amaiz-backend-ms-prod.at-azure-amaiz-55185456.corp.amdocs.azr/api/v1/chats/status/{task_id}"
status_headers = {
    'accept': 'application/json',
}

# Loop to get status of the task_id until the status is Complete
result = ""
while True:
    chat_results = requests.get(status_url, headers=status_headers, verify=ca_bundle_path)
    chat_data = chat_results.json()
    print(chat_data)
    if chat_data.get("status") == "Complete":
        result = chat_data.get("result")
        break
    time.sleep(1)

print("Result: ", result)
