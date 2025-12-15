# Harness Chaos Template Creator

A Python utility to create Chaos Experiment Templates in Harness at the Account level by reading configurations from a local JSON file. This script handles the specific JSON payload formatting required by the Harness Chaos Manager API.

## Prerequisites

  * **Python 3.6+**
  * **Harness Account ID** (Found in your Harness URL)
  * **Harness API Key** (Personal Access Token or Service Account Token)

## Installation

1.  **Download the script**: Save the python code as `create_template.py`.
2.  **Install dependencies**:
    ```bash
    pip install requests
    ```

## Setup

### 1\. Create your Configuration File

Create a file named `experiment_config.json`. This file should contain the standard JSON definition of your experiment.

**Example content for `experiment_config.json`:**

```json
{
  "apiVersion": "litmuschaos.io/v1beta1",
  "kind": "ChaosExperimentTemplate",
  "identity": "poddeletetemplate",
  "name": "pod-delete-template",
  "revision": "v1",
  "isDefault": true,
  "spec": {
    "infraType": "KubernetesV2",
    "actions": [],
    "faults": [
      {
        "name": "pod-delete-fault",
        "identity": "pod-delete",
        "revision": "v1",
        "values": [
          { "name": "TOTAL_CHAOS_DURATION", "value": "30" }
        ]
      }
    ],
    "cleanupPolicy": "delete"
  }
}
```

## Usage

Run the script from your terminal using the following arguments:

```bash
python3 create_template.py \
  --account-id "YOUR_ACCOUNT_ID" \
  --api-key "YOUR_API_KEY" \
  --file "experiment_config.json"
```

### Argument Reference

| Argument | Description | Required |
| :--- | :--- | :--- |
| `--account-id` | Your Harness Account Identifier (e.g., `Pt_YA3a...`). | **Yes** |
| `--api-key` | Your Harness API Token (starts with `pat.` or `sat.`). | **Yes** |
| `--file` | Path to your local JSON config file. | **Yes** |
| `--url` | Base URL. Default: `https://app.harness.io`. Change if using a different environment. | No |

## Troubleshooting

  * **401 Unauthorized**:
      * Verify your API Key is correct.
      * Ensure the API Key has **Chaos Engineering \> Template \> Create** permissions.
  * **400 Bad Request / 500 Error**:
      * Validate your `experiment_config.json` syntax.
      * Ensure mandatory fields like `infraType` and `apiVersion` are present in the JSON.
