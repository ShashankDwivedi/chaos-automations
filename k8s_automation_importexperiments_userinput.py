#Author: Shashank Dwivedi, Senior Technical Program Manager, Harness
import requests
import json
import argparse
import uuid

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

            unique_suffix = str(uuid.uuid4())[:8]

            name = template_identity+'-'+unique_suffix

            Experiment_Templates_Import_Body = json.dumps(
                {
                    "accountIdentifier": account_id,
                    "infraRef": infra_ref,
                    "organizationIdentifier": org,
                    "projectIdentifier": proj,
                    "importType":"LOCAL",
                    "name": name,
                    "identity": name
                }

                )

            print('Going to Import Template:: ', template_identity)

            import_template_url = BASE_URL_TEMPLATES+'/'+template_identity+'/launch'

            response = requests.request('POST',import_template_url,params=params,headers=chaos_headers,data=Experiment_Templates_Import_Body)

            print(response.text)
    except Exception as e:

        print('Exception Occured While Importing Experiment',e)

if __name__ == "__main__":

    ACCOUNT_IDENTIFIER = 'Your Account Identifier'

    API_TOKEN = "Your API Token"

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

