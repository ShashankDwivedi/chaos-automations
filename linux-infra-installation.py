#Author Shashank Dwivedi, Senior Technical Program Manager, Harness
import requests
import paramiko
import time
import argparse

API_TOKEN = "Your API Token"

ACCOUNT_IDENTIFIER = 'Your Account ID'

LINUX_BASE_URL = 'https://app.harness.io/gateway/chaos/manager/api/query?routingId=<YourAccountID>'

def run_remote_command_with_password(host, user, password,root_password,remote_command):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, username=user,password=password)

    # Start interactive shell
    shell = ssh_client.invoke_shell()

    # Wait for shell prompt
    time.sleep(5)
    shell.recv(1000)

    # Step 1: Switch to root
    shell.send("sudo su -\n")
    time.sleep(10)

    # Send sudo password
    shell.send(root_password + "\n")
    time.sleep(10)

    output = shell.recv(5000).decode()

    # Step 2: Execute command as root
    shell.send(remote_command + "\n")
    time.sleep(10)

    output += shell.recv(5000).decode()

    print('Output is', output)

    # Exit root shell
    shell.send("exit\n")
    time.sleep(1)
    shell.recv(1000)

    ssh_client.close()

    
def generate_remote_command(orgId,projectId,envId,infra_name):

    GRAPH_QL_QUERY = """
        mutation registerLinuxInfra(
        $request: RegisterLinuxInfraRequest!,
        $identifiers: IdentifiersRequest!,

            ) 
        {
        registerLinuxInfra(
        identifiers: $identifiers,
        request: $request
    ) {
        infraID
        name
        accessKey
        serverURL
        version
    }
    }
    """

    VARIABLES = {

        "identifiers": {
                "orgIdentifier": orgId,
                "accountIdentifier": ACCOUNT_IDENTIFIER,
                "projectIdentifier": projectId
        },
        "request": {
                "name": infra_name,
                "environmentID": envId,
                "description": "Linux Infra Through API Call"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_TOKEN
    }

    response = requests.post(LINUX_BASE_URL,headers=headers,json={"query": GRAPH_QL_QUERY, "variables": VARIABLES})

    response = response.json()['data']['registerLinuxInfra']

    linux_infra_id = response['infraID']

    linux_access_key = response['accessKey']

    linux_agent_version = response['version']

    linux_server_url = response['serverURL']

    COMMAND_EXECUTE_LINUX = 'curl https://app.harness.io/public/shared/tools/chaos/linux/'+linux_agent_version+'/install.sh'+' | sudo bash /dev/stdin --infra-id '+linux_infra_id+' --access-key '+linux_access_key+' --account-id '+ACCOUNT_IDENTIFIER+' --server-url '+linux_server_url

    return COMMAND_EXECUTE_LINUX

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Sample script to read arguments from user"
    )

    # Add arguments
    parser.add_argument("--orgId", required=True, help="Organization Identifier")
    parser.add_argument("--projectId",required=True, help="Project Identifier")
    parser.add_argument("--envId", required=True, help="Environment Identifier")
    parser.add_argument("--infraName",required=True, help="Infra Name")
    

    # Parse arguments
    args = parser.parse_args()

    remote_command = generate_remote_command(args.orgId,args.projectId,args.envId,args.infraName)

    print('Remote Command \n')

    print(remote_command)

    host_name = ''
    user = ''
    password = ''
    root_password=''

    run_remote_command_with_password(host_name,user,password,root_password,remote_command)
