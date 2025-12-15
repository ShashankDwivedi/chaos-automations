# Harness Chaos Experiment Bulk Importer - create_experiments_template.py

**Author**: Shashank Dwivedi, Senior Technical Program Manager, Harness

This automation script facilitates the **bulk propagation of Chaos Experiment Templates** across an entire Harness Account. It traverses the account hierarchy (Organizations → Projects → Environments → Infrastructures), identifies infrastructures where **Chaos V2 is enabled**, and automatically imports/launches experiments from a Account Scoped Chaos Hub.

---

## 🚀 Capabilities

* **Deep Discovery**: Recursively fetches all Organizations, Projects, and Environments within the account.
* **Smart Filtering**: Targets only infrastructures where the Harness Chaos (V2) module is explicitly enabled (`isChaosEnabled=True`).
* **Bulk Instantiation**: Fetches all templates from a specific **Chaos Hub** and instantiates them as experiments in the target projects.

---

## 📋 Prerequisites

* **Python 3.6+**
* **Harness Account Access**:
    * Account Identifier
    * API Key (Personal Access Token or Service Account Token) with permissions to:
        * Read Organizations, Projects, and Environments.
        * Create and Manage Chaos Experiments.
* **Dependencies**:
    ```bash
    pip install requests
    ```

---

## ⚙️ Configuration

Before running the script, open `create_experiments_template.py` and configure the following global variables:

### 1. Authentication & Account
Update the credentials at the top of the file:

```python
# Your Harness Account ID (found in URL or Account Settings)
ACCOUNT_IDENTIFIER = 'SxuV0ChbRqWGSYClFlMQMQ'

# Your Harness API Token (Keep this secret!)
API_TOKEN = "<Your Token>"
