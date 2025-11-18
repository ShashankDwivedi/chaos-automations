#Author: Shashank Dwivedi, Senior Technical Program Manager, Harness

import requests
import json

ACCOUNT_IDENTIFIER = 'SxuV0ChbRqWGSYClFlMQMQ'

API_TOKEN = "<Your Token>"

BASE_URL_TEMPLATES = 'https://app.harness.io/gateway/chaos/manager/api/rest/experimenttemplates'

BASE_URL_PROJECTS = 'https://app.harness.io/v1/orgs/default/projects?'

BASE_URL_ORG = 'https://app.harness.io/v1/orgs'

BASE_ENV_URL = 'https://app.harness.io/ng/api/environmentsV2'

BASE_CHAOS_V2_INFRA_ENABLED = 'https://app.harness.io/gateway/chaos/manager/api/rest/v2/infrastructures'

common_headers = {
    'Harness-Account': ACCOUNT_IDENTIFIER,
    'x-api-key': API_TOKEN
}

CHAOS_HUB_REF = 'ShashankHubAccount'

orgs_projects = {}

# The Purpose of This Function is to do an API Call to Fetch the List of Orgs
# After fetching the List of Orgs, This functions loops over Org List to Find List of Projects
def start_automation_process():

    response = requests.request('GET',BASE_URL_ORG,headers=common_headers)

    for org in response.json():

        org = org['org']['identifier']

        get_list_projects(org)

# Argument: Accepts an OrgName <String>
# The Purpose of This Function is to do an API Call to Fetch the List of of Projects within an Org
# After fetching the List of Projects, This functions loops over Project List and calls get_environment_chos_infra function to get the enviroment and infra details
def get_list_projects(org):

    project_list = []

    PROJECT_URL = BASE_URL_ORG+'/'+org+'/projects'

    response = requests.request('GET', PROJECT_URL, headers=common_headers)

    for key in response.json():

        project_name=key['project']['identifier']

        get_environments_chaos_infra(org,project_name)


#Argument: org name and project name
#The purpose of this function is to get the environment id and call the filter_populate_chaosv2_infra() function to get the infra level details
def get_environments_chaos_infra(org,project_name):

    params = {
        'accountIdentifier': ACCOUNT_IDENTIFIER,
        'orgIdentifier': org,
        'projectIdentifier': project_name
    }

    env_headers = {
        'x-api-key': API_TOKEN
    }

    response = requests.request('GET',BASE_ENV_URL, params=params, headers=env_headers)

    for env in response.json()['data']['content']:

        environment_identifier = env['environment']['identifier']

        filter_populate_chaosv2infra(org,project_name,environment_identifier)
    

#Argument: org name, project name and environment identifier
#The purpose of this function is to find the list of infra that are on ChaosV2 where Chaos is Enbaled (True)
#Finally the function generate a Key which is a combination of Org, Project , EnvironmentIdentifier/Infraidentifier and calls the create_experiment_from_template() function
def filter_populate_chaosv2infra(org,project_name,env_identifier):

    try:
        params = {
        'accountIdentifier': ACCOUNT_IDENTIFIER,
        'orgIdentifier': org,
        'projectIdentifier': project_name,
        'organizationIdentifier': org,
        'page':0,
        'limit':15,
        'search':"",
        'environmentIdentifier': env_identifier,
        'includeLegacyInfra': False
        }

        payload = {}

        proj_headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_TOKEN
        }
        response = requests.request('POST',BASE_CHAOS_V2_INFRA_ENABLED, params=params,headers=proj_headers,json=payload)
        for infra in response.json()['infras']:

            try:

                if(infra['isChaosEnabled']==True):

                    org_proj_env_infra_key = org+':'+project_name+':'+env_identifier+'/'+infra['infraID']

                    create_experiment_from_template(org_proj_env_infra_key)
                else:
                    continue
            except:
                continue
    except:
        print('Exception Found for Org: ',org+' And project: '+project_name)


#Argument: org_proj_infrakey | Example defaultorg:defaultproj:myenv/myinfra
# The purpose of this function is to iterate over all the experiment templates present in Chaos Hub and create experiments in the respective projects.
def create_experiment_from_template(org_proj_infrakey):

    try:

        org = org_proj_infrakey.split(':')[0]

        proj = org_proj_infrakey.split(':')[1]

        infra_ref = org_proj_infrakey.split(':')[2]

        params = {
      
        "accountIdentifier": ACCOUNT_IDENTIFIER,
        "organizationIdentifier": "",
        "projectIdentifier": "",
        "hubIdentity": CHAOS_HUB_REF,
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

    start_automation_process()


