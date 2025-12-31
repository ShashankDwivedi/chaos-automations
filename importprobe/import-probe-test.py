#Author, Shashank Dwivedi, Senior Technical Program Manager, Harness
import requests
import json
import argparse

API_TOKEN = "Your API Token"

ACCOUNT_IDENTIFIER = 'Your Account ID'

Probe_Import_Url = "https://app.harness.io/gateway/chaos/manager/api/rest/v2/probes/import"

List_Probes_From_Templates_EndPoint = 'https://app.harness.io/gateway/chaos/manager/api/rest/templates/probes'

def import_probes_from_templates(org_id,project_id,chaos_hub_id):
    
  probes_list_params = {
      "accountIdentifier": ACCOUNT_IDENTIFIER,
      "organizationIdentifier":"",
      "projectIdentifier": "",
      "hubIdentity": chaos_hub_id
  }

  probes_import_params = {

    "accountIdentifier": ACCOUNT_IDENTIFIER,
    "organizationIdentifier":org_id,
    "projectIdentifier": project_id   
  }

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-API-KEY': API_TOKEN
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
          "accountID": ACCOUNT_IDENTIFIER,
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

  parser = argparse.ArgumentParser(description="Sample script to read arguments from user")

  # Add arguments
  parser.add_argument("--orgId", required=True, help="Organization Identifier")
  parser.add_argument("--projectId",required=True, help="Project Identifier")
  parser.add_argument("--chaoshubId",required=True, help="Chaos Hub Identifier")
    

  # Parse arguments
  args = parser.parse_args()

  import_probes_from_templates(args.orgId,args.projectId,args.chaoshubId)
