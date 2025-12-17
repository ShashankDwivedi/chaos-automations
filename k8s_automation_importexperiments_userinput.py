#Author: Shashank Dwivedi, Senior Technical Program Manager, Harness

import requests
import json
import argparse
import random

BASE_URL_TEMPLATES = 'https://app.harness.io/gateway/chaos/manager/api/rest/experimenttemplates'

#Argument: org_proj_infrakey | Example defaultorg:defaultproj:myenv/myinfra
# The purpose of this function is to iterate over all the experiment templates present in Chaos Hub and create experiments in the respective projects.
def create_experiment_from_template(account_id,org,proj,env_id,infra_id,chaos_hub,api_token):

    try:

        infra_ref = env_id+'/'+infra_id

        params = {
      
        "accountIdentifier": account_id,
        "organizationIdentifier": "",
        "projectIdentifier": "",
        "hubIdentity": chaos_hub,
        "revision": "v1",
        "verbose": False
        }
        chaos_headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_token
         }

        templates_list = requests.request('GET',BASE_URL_TEMPLATES,params=params,headers=chaos_headers)

        for data in templates_list.json()['data']:

            template_identity = data['identity']

            name = template_identity+'-'+str(random.randint(1,10))

            Experiment_Templates_Import_Body = json.dumps(
                {
                    "accountIdentifier": account_id,
                    "infraRef": infra_ref,
                    "organizationIdentifier": org,
                    "projectIdentifier": proj,
                    "importType":"REFERENCE",
                    "name": name,
                    "identity": name
                }

                )

            print('Going to Import Template:: ', template_identity)

            import_template_url = BASE_URL_TEMPLATES+'/'+template_identity+'/launch'

            response = requests.request('POST',import_template_url,params=params,headers=chaos_headers,data=Experiment_Templates_Import_Body)

            print(response.text)
    except:

        print('Exception Occured While Creating Experiment for ORG: '+org+'Project: '+proj+'InfraRef: '+infra_ref)

if __name__ == "__main__":

    ACCOUNT_IDENTIFIER = 'SxuV0ChbRqWGSYClFlMQMQ'

    API_TOKEN = "pat.SxuV0ChbRqWGSYClFlMQMQ.6915a15f5176ec4f502fe8f6.xXH1gkbbuSWnIkv6mhgQ"

    parser = argparse.ArgumentParser(description="Sample script to read arguments from user")

    # Add arguments
    parser.add_argument("--orgId", required=True, help="Organization Identifier")
    parser.add_argument("--projectId",required=True, help="Project Identifier")
    parser.add_argument("--envId", required=True, help="Environment Identifier")
    parser.add_argument("--infraId",required=True, help="Infra Identifier")
    parser.add_argument("--chaoshubId",required=True, help="Chaos Hub Identifier")
    

    # Parse arguments
    args = parser.parse_args()

    create_experiment_from_template(ACCOUNT_IDENTIFIER,args.orgId,args.projectId,args.envId,args.infraId,args.chaoshubId,API_TOKEN)

