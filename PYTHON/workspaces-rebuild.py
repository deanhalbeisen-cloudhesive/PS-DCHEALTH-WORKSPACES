import boto3
from botocore.exceptions import BotoCoreError, ClientError
import time

# Configuration and constants
AWS_REGION = "us-west-2"
MAX_RETRIES = 3
RETRY_DELAY = 10  # Delay between retries in seconds

# Initialize the Boto3 client for Amazon WorkSpaces
client = boto3.client('workspaces', region_name=AWS_REGION)

def rebuild_workspace(workspace_id):
    """
    Rebuilds a single workspace by its ID, with retries on failure.

    Args:
    workspace_id (str): The ID of the workspace to rebuild.

    Returns:
    bool: True if rebuild was successful, False otherwise.
    """
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            response = client.rebuild_workspaces(
                RebuildWorkspaceRequests=[
                    {
                        'WorkspaceId': workspace_id
                    },
                ]
            )
            print(f"Rebuild initiated successfully for Workspace ID: {workspace_id}")
            return True
        except (BotoCoreError, ClientError) as error:
            print(f"Failed to rebuild Workspace ID: {workspace_id}, Attempt: {attempt + 1}")
            print(f"Error: {error}")
            time.sleep(RETRY_DELAY)
            attempt += 1
    return False

def rebuild_workspaces(workspace_ids):
    """
    Rebuilds a list of workspaces.

    Args:
    workspace_ids (list of str): The list of workspace IDs to rebuild.

    Returns:
    dict: A dictionary reporting the rebuild status for each workspace ID.
    """
    statuses = {}
    for workspace_id in workspace_ids:
        status = rebuild_workspace(workspace_id)
        statuses[workspace_id] = 'Success' if status else 'Failed'
    return statuses

# Example usage
workspace_ids = ['ws-123', 'ws-456', 'ws-789']
statuses = rebuild_workspaces(workspace_ids)
print("Rebuild statuses:", statuses)
