import requests
import json
import argparse
import sys
import os

def create_chaos_template(api_url, account_id, api_key, file_path, hub_identity="Custom_Templates"):
    """
    Creates a Harness Chaos Experiment Template at the Account level.
    """
    
    # 1. Endpoint Configuration
    # The endpoint from your curl command
    endpoint = f"{api_url}/gateway/chaos/manager/api/rest/experimenttemplates"
    
    # Query Parameters
    params = {
        "hubIdentity": hub_identity,
        "accountIdentifier": account_id,
        "organizationIdentifier": "", # Empty for Account level
        "projectIdentifier": ""       # Empty for Account level
    }

    # 2. Read and Parse the Config File
    try:
        with open(file_path, 'r') as f:
            experiment_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON from '{file_path}'.\nDetails: {e}")
        sys.exit(1)

    # 3. Construct Payload
    # CRITICAL: The API expects the 'manifest' key to contain the *stringified* JSON of the experiment.
    # We use json.dumps() to convert the dict back to a string.
    payload = {
        "manifest": json.dumps(experiment_data)
    }

    # 4. Headers
    # Note: It is best practice to use x-api-key for scripts, but Authorization: Bearer works for session tokens.
    headers = {
        "Content-Type": "application/json",
        "harness-account": account_id,
        "x-api-key": api_key  # Using standard API Key header
        # If using a session token (like your curl), change the line above to:
        # "Authorization": f"Bearer {api_key}" 
    }

    # 5. Make the Request
    try:
        print(f"Sending request to {endpoint}...")
        response = requests.post(
            endpoint, 
            params=params, 
            headers=headers, 
            json=payload
        )

        # 6. Handle Response
        if response.status_code in [200, 201]:
            print("SUCCESS: Experiment Template created successfully.")
            print("Response:", response.json())
        else:
            print(f"FAILED: Status Code {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Harness Chaos Experiment Template')
    
    parser.add_argument('--account-id', required=True, help='Harness Account Identifier')
    parser.add_argument('--api-key', required=True, help='Harness API Key (or PAT)')
    parser.add_argument('--file', required=True, help='Path to the JSON config file')
    parser.add_argument('--url', default='https://app.harness.io', help='Base URL (default: https://app.harness.io)')
    
    args = parser.parse_args()

    create_chaos_template(
        api_url=args.url,
        account_id=args.account_id,
        api_key=args.api_key,
        file_path=args.file
    )
