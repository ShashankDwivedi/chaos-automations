#Author: Shashank Dwivedi, Senior Technical Program Manager, Harness
#The purpose of this python script is to automate the installation of Windows Infrastructure
import requests
import winrm
import time

INVOKE_REQUEST = "powershell -Command & { Invoke-WebRequest -Uri"

EXECUTION_COMMAND = "-Outfile install.ps1 -UseBasicParsing; .\install.ps1"

END_SEPERATOR = '}'

def get_powershell_command(account_id,org_id,project_id,api_url,api_token,infra_name,env_id):

    params = {
                "accountIdentifier": account_id,
                "orgIdentifier": org_id,
                "projectIdentifier": project_id,
                "organizationIdentifier": org_id,
                "infraType": "Windows"
    
            }

    headers = {
                'Content-Type': 'application/json',
                'x-api-key': api_token,
                'Harness-Account': account_id
            }

    payload = {
                "name": infra_name,
                "environmentID": env_id,
                "description": "API",
                "infraType": "Windows"
            }

    response = requests.post(api_url,params=params,headers=headers,json=payload)

    response = response.json()

    infra_id = response['infraID']

    access_key = response['accessKey']

    version = response['version']

    server_url = response['serverURL']

    INSTALLATION_URL = 'https://app.harness.io/public/shared/tools/chaos/windows/'+version+'/install.ps1'

    POWER_SHELL_COMMAND = f"""

    {INVOKE_REQUEST} {INSTALLATION_URL} {EXECUTION_COMMAND} -InfraId {infra_id} -AccessKey {access_key} -AccountID {account_id} -ServerUrl {server_url} {END_SEPERATOR}

    """

    return POWER_SHELL_COMMAND

def winrm_login_invoke_powershell(host,username,password,powershell_command):

    try:
        # Create WinRM session
        session = winrm.Session(
            target=host,
            auth=(username, password),
            transport='ntlm'
        )

        # Execute PowerShell command
        result = session.run_ps(powershell_command)

        time.sleep(30)

        print("STATUS CODE:", result.status_code)
        print("STDOUT:\n", result.std_out.decode())
        print("STDERR:\n", result.std_err.decode())

    except Exception as e:
        print("Error occurred:", str(e))



if __name__ == '__main__':

    WINDOWS_BASE_URL = 'https://app.harness.io/gateway/chaos/manager/api/rest/machine/infra'

    API_TOKEN = "Your API Token"

    ACCOUNT_IDENTIFIER = 'Your Account ID'

    ORG_IDENTIFIER = 'Your ORG ID'

    PROJECT_IDENTFIER = 'Your Project ID'

    INFRA_NAME = 'Your Infra Name'

    ENV_ID = 'Your Environment ID'

    HOST = ''

    USER_NAME = ''

    PASSWORD = ''

    powershell_command = get_powershell_command(ACCOUNT_IDENTIFIER,ORG_IDENTIFIER,PROJECT_IDENTFIER,WINDOWS_BASE_URL,API_TOKEN,INFRA_NAME,ENV_ID)

    print('Poweshell Command Is \n')

    print(powershell_command)

    winrm_login_invoke_powershell(HOST,USER_NAME,PASSWORD,powershell_command)


