#Author: Shashank Dwivedi, Senior Technical Program Manager, Harness
#Arguments Needed while running the script
# orgId, projectId, envId, infraId, chaoshubId

import requests
import json
import argparse

ACCOUNT_IDENTIFIER = 'SxuV0ChbRqWGSYClFlMQMQ'

API_TOKEN = "Your API Token "

BASE_URL_TEMPLATES = 'https://app.harness.io/gateway/chaos/manager/api/rest/experimenttemplates'


common_headers = {
    'Harness-Account': ACCOUNT_IDENTIFIER,
    'x-api-key': API_TOKEN
}
def create_experiment_from_template(org,proj,env_id,infra_id,chaos_hub):

    try:

        infra_ref = env_id+'/'+infra_id

        params = {
      
        "accountIdentifier": ACCOUNT_IDENTIFIER,
        "organizationIdentifier": "",
        "projectIdentifier": "",
        "hubIdentity": chaos_hub,
        "revision": "v1",
        "verbose": False
        }
        chaos_headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': API_TOKEN
         }

        Experiment_Templates_Import_Body = json.dumps(
            {
            "accountIdentifier": ACCOUNT_IDENTIFIER,
            "infraRef": infra_ref,
             "organizationIdentifier": org,
             "projectIdentifier": proj
            }
        )

        templates_list = requests.request('GET',BASE_URL_TEMPLATES,params=params,headers=chaos_headers)

        for data in templates_list.json()['data']:

            template_identity = data['identity']

            import_template_url = BASE_URL_TEMPLATES+'/'+template_identity+'/launch'

            response = requests.request('POST',import_template_url,params=params,headers=chaos_headers,data=Experiment_Templates_Import_Body)

            print(response.text)
    except:

        print('Exception Occured While Creating Experiment for ORG: '+org+'Project: '+proj+'InfraRef: '+infra_ref)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Sample script to read arguments from user"
    )

    # Add arguments
    parser.add_argument("--orgId", required=True, help="Organization Identifier")
    parser.add_argument("--projectId",required=True, help="Project Identifier")
    parser.add_argument("--envId", required=True, help="Environment Identifier")
    parser.add_argument("--infraId",required=True, help="Infra Identifier")
    parser.add_argument("--chaoshubId",required=True, help="Chaos Hub Identifier")
    

    # Parse arguments
    args = parser.parse_args()

    create_experiment_from_template(args.orgId,args.projectId,args.envId,args.infraId,args.chaoshubId)

