import requests
import json
import uuid
import os
import sys

# Author: Shashank Dwivedi, Senior Technical Program Manager, Harness
# Improved Version

BASE_URL_TEMPLATES = 'https://app.harness.io/gateway/chaos/manager/api/rest/experimenttemplates'

def create_experiment_from_template(account_id, org, proj, env_id, infra_id, chaos_hub, api_token):
    """
    Iterates over all experiment templates in the specified Chaos Hub
    and launches them into the target Infrastructure.
    """
    infra_ref = f"{env_id}/{infra_id}"
    
    print(f"--- Starting Import Process ---")
    print(f"Target: Org={org}, Proj={proj}, Infra={infra_ref}")

    params = {
        "accountIdentifier": account_id,
        "organizationIdentifier": "", # Intentionally empty as per API requirement for Hub fetch
        "projectIdentifier": "",      # Intentionally empty as per API requirement for Hub fetch
        "hubIdentity": chaos_hub,
        "revision": "v1",
        "verbose": False
    }

    chaos_headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_token
    }

    try:
        # 1. Fetch List of Templates from the Hub
        print(f"Fetching templates from Hub: {chaos_hub}...")
        templates_response = requests.get(
            BASE_URL_TEMPLATES, 
            params=params, 
            headers=chaos_headers, 
            verify=False
        )
        templates_response.raise_for_status() # Raise error if request failed
        
        templates_data = templates_response.json().get('data', [])
        
        if not templates_data:
            print("No templates found in the specified Chaos Hub.")
            return

        print(f"Found {len(templates_data)} templates. Beginning import...")

        # 2. Iterate and Import Each Template
        for data in templates_data:
            template_identity = data['identity']
            
            # Generate a unique name to prevent collisions
            # Using UUID instead of random int for better uniqueness
            unique_suffix = str(uuid.uuid4())[:8]
            new_experiment_name = f"{template_identity}-{unique_suffix}"

            payload = {
                "accountIdentifier": account_id,
                "infraRef": infra_ref,
                "organizationIdentifier": org,
                "projectIdentifier": proj,
                "name": new_experiment_name,
                "identity": new_experiment_name
            }

            print(f"Importing Template: {template_identity} -> New Name: {new_experiment_name}")

            import_url = f"{BASE_URL_TEMPLATES}/{template_identity}/launch"
            
            import_response = requests.post(
                import_url, 
                params=params, 
                headers=chaos_headers, 
                data=json.dumps(payload), 
                verify=False
            )

            if import_response.status_code == 200:
                print(f"✅ Success: {new_experiment_name}")
            else:
                print(f"❌ Failed: {import_response.status_code} - {import_response.text}")

    except requests.exceptions.RequestException as e:
        print(f"🔥 Network/API Error: {e}")
    except Exception as e:
        print(f"🔥 General Error: {e}")

def validate_env_vars():
    """
    Ensures all required environment variables are set.
    Returns a dictionary of vars if successful, exits if failed.
    """
    required_vars = [
        'API_TOKEN', 'ORG_ID', 'PROJECT_ID', 
        'ENV_ID', 'INFRA_ID', 'CHAOSHUB_ID', 'ACCOUNT_ID'
    ]
    
    env_vars = {}
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        env_vars[var] = value

    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
        
    return env_vars

if __name__ == "__main__":
    # Validate and load variables
    config = validate_env_vars()

    # Run the import
    create_experiment_from_template(
        account_id=config['ACCOUNT_ID'],
        org=config['ORG_ID'],
        proj=config['PROJECT_ID'],
        env_id=config['ENV_ID'],
        infra_id=config['INFRA_ID'],
        chaos_hub=config['CHAOSHUB_ID'],
        api_token=config['API_TOKEN']
    )
