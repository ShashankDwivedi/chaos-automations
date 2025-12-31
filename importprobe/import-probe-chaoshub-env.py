#Author, Shashank Dwivedi, Senior Technical Program Manager, Harness
import requests
import json
import os

Probe_Import_Url = "https://app.harness.io/gateway/chaos/manager/api/rest/v2/probes/import"

List_Probes_From_Templates_EndPoint = 'https://app.harness.io/gateway/chaos/manager/api/rest/templates/probes'

def import_probes_from_templates(org_id,project_id,chaos_hub_id,token,account_id):
    
  probes_list_params = {
      "accountIdentifier": account_id,
      "organizationIdentifier":"",
      "projectIdentifier": "",
      "hubIdentity": chaos_hub_id
  }

  probes_import_params = {

    "accountIdentifier": account_id,
    "organizationIdentifier":org_id,
    "projectIdentifier": project_id   
  }

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-API-KEY': token
  }

  probes_response = requests.request('GET',List_Probes_From_Templates_EndPoint,params=probes_list_params,headers=headers,verify=False)

  for data in probes_response.json()['data']:

    try:
      probe_identity= data['identity']
      probe_name = data['name']
      payload = json.dumps({
        "identity": probe_identity,
        "importType": "LOCAL",
        "name": probe_name,
        "probeRef": probe_identity,
        "hubIdentifiers": {
          "accountID": account_id,
          "orgID": "",
          "projectID": ""
        },
        "hubRef": chaos_hub_id
      })
      response = requests.request("POST",Probe_Import_Url,params=probes_import_params,headers=headers,data=payload,verify=False)
      print(response.text)
    except Exception as e:
      print('Exception Message is:',e)
      continue


  
if __name__ == "__main__":

  # Read Environment Variables

  org_id = os.getenv('ORG_ID')

  project_id = os.getenv('PROJECT_ID')

  chaoshub_id = os.getenv('CHAOSHUB_ID')

  token = os.getenv('API_TOKEN')

  account_id = os.getenv('ACCOUNT_ID')

  import_probes_from_templates(org_id,project_id,chaoshub_id,token,account_id)
