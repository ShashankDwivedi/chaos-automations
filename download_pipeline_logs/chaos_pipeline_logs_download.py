#Author: Shashank Dwivedi, Senior Customer Architect, Harness Inc.
# The purpose of this script is to demonstrate how to trigger a chaos pipeline in Harness using a custom webhook, fetch pipeline execution details using the trigger event correlation id, extract log keys and chaos metadata from the execution graph using JSONPath, download logs using log keys and save them in a file named after the experiment run id which can be used for further analysis like extracting actual resilience score from logs and comparing it with expected resilience score.
import requests
from jsonpath_ng import jsonpath, parse
import time
import json

ACCOUNT_ID = "Your Account ID"
ORG_ID = "Your ORG ID Where Your Pipeline to trigger Chaos Is"
PROJECT_ID = "Your Project ID Where Your Pipeline Is"
PIPELINE_ID = "Your Pipeline ID"
TRIGGER_ID = "Your Custom Trigger ID"
API_TOKEN = "Your API Token"
COMMON_HEADERS = {"x-api-key": API_TOKEN}
chaos_metadata = {}

#The purpose of this fn is to trigger the pipeline and return the trigger event correlation id which can be used to fetch pipeline execution details and logs
def get_trigger_event_id():
    # 1. Define the Webhook URL
    url = "https://app.harness.io/gateway/pipeline/api/webhook/custom/fSiTbLPrRE-M9KfnK8CV_Q/v3"
    # 2. Define the Query Parameters (from the URL string)
    params = {
        "accountIdentifier": ACCOUNT_ID,
        "orgIdentifier": ORG_ID,
        "projectIdentifier": PROJECT_ID,
        "pipelineIdentifier": PIPELINE_ID,
        "triggerIdentifier": TRIGGER_ID
    }

    # 3. Define the Headers
    trigger_headers = {
        "Content-Type": "application/json"
    }

    # 4. Define the JSON Payload (the -d data)
    trigger_payload = {
        "infra": "chaosdemo/shashankchaosinfra",
        "namespace": "harness",
        "workload": "nginx-deployment"
    }


    # 5. Execute the POST request
    trigger_response = requests.post(url, params=params, headers=trigger_headers, data=json.dumps(trigger_payload))

    trigger_event_correlation_id = trigger_response.json()['data']['eventCorrelationId']

    print(f"Pipeline triggered successfully! TriggerEvent ID: {trigger_event_correlation_id}")

    return trigger_event_correlation_id

#The purpose of this fn is to fetch pipeline execution details using the trigger event correlation id and extract log keys and chaos metadata from the execution graph using JSONPath
def get_pipeline_execution_id(trigger_event_correlation_id):

    webhook_url = "https://app.harness.io/pipeline/api/webhook/triggerExecutionDetails/" + trigger_event_correlation_id

    webhook_data= {
    "accountIdentifier": ACCOUNT_ID
    }

    webhook_headers = {"x-api-key": API_TOKEN}

    webhook_response = requests.get(webhook_url, headers=webhook_headers, params=webhook_data)

    webhook_data = webhook_response.json()

    pipeline_execution_id = webhook_data['data']['webhookProcessingDetails']['pipelineExecutionId']

    return pipeline_execution_id

# The purpose of this fn is to fetch log keys from the execution graph using JSONPath and then use those log keys to download logs and save them in a file. This fn also extracts chaos metadata like expected resilience score and actual resilience score from the execution graph using JSONPath and saves it in a dictionary. Finally, it saves the downloaded logs in a file named after the experiment run id which can be used for further analysis like extracting actual resilience score from logs and comparing it with expected resilience score.
def get_log_keys(pipeline_execution_id):
    pipeline_execution_url = "https://app.harness.io/pipeline/api/pipelines/execution/v2/" + pipeline_execution_id

    pipeline_details_params = {
    "accountIdentifier": ACCOUNT_ID,
    "orgIdentifier": ORG_ID,
    "projectIdentifier": PROJECT_ID,
    "renderFullBottomGraph": "true"
    }   
    response = requests.get(pipeline_execution_url, headers=COMMON_HEADERS, params=pipeline_details_params)

    data = response.json()

    data = data['data']['executionGraph']['nodeMap']

    # Find Log Keys using JSONPath

    jsonpath_logkeys = parse('$..logKeys')

    # Execute search
    matches = jsonpath_logkeys.find(data)

    # Extract values
    log_key_ids = [match.value for match in matches]

    log_key_ids = list(filter(None, log_key_ids))

    # Flattens the nested structure into one long list of strings
    log_key_ids = [item for sublist in log_key_ids for item in sublist]

    print("Log Keys found in the execution graph:",log_key_ids)

    # Find expected resileince score and resilience score using JSONPath

    chaos_data = parse('$..[infraReference,experimentRunId,expectedResilienceScore,resiliencyScore]')

    # Execute search
    matches = chaos_data.find(data)

    # Extract values
    for match in matches:
        chaos_metadata[match.path.fields[-1]] = match.value

    print("Chaos Metadata found in the execution graph:",chaos_metadata)

    FILE_NAME = "experiment_execution_"+str(chaos_metadata['experimentRunId'])+".log"

    print(f"Saving chaos metadata to file: {FILE_NAME}")

    save_chaos_execution_logs(log_key_ids,FILE_NAME)


#The purpose of this fn is to download logs using log keys and save them in a file named after the experiment run id which can be used for further analysis like extracting actual resilience score from logs and comparing it with expected resilience score.
def save_chaos_execution_logs(log_key_ids,FILE_NAME):

    logs_download_url = 'https://app.harness.io/gateway/log-service/blob'

    for log_key in log_key_ids:
        params_logs = {
            "accountID": ACCOUNT_ID,
            "orgId": ORG_ID,
            "projectId": PROJECT_ID,
            "pipelineId": PIPELINE_ID,
            "key": log_key
        }
        response = requests.get(logs_download_url, headers=COMMON_HEADERS, params=params_logs)

        time.sleep(10) # Sleep for 10 seconds between log download requests to avoid hitting rate limits

        with open(FILE_NAME, "a", encoding="utf-8") as file_handler:
            file_handler.write(response.text + "\n")

if __name__ == "__main__":

    trigger_event_id = get_trigger_event_id()

    time.sleep(360) # User should adjust this time based on the complexity of the pipeline and expected execution time of the chaos experiment

    pipeline_execution_id = get_pipeline_execution_id(trigger_event_id)

    get_log_keys(pipeline_execution_id)
