import boto3
import time
from botocore.exceptions import BotoCoreError, ClientError

# Initialize a boto3 client for Amazon WorkSpaces
client = boto3.client('workspaces')

def delete_workspace(workspace_id):
    """
    Delete a specific AWS Workspace by its ID.
    
    Parameters:
        workspace_id (str): The ID of the workspace to be deleted.
        
    Returns:
        None
    """
    try:
        # Attempt to delete the workspace
        response = client.terminate_workspaces(
            TerminateWorkspaceRequests=[
                {
                    'WorkspaceId': workspace_id
                },
            ]
        )
        # Check for unsuccessful deletions
        unsuccessful_deletions = response.get('FailedRequests', [])
        if unsuccessful_deletions:
            print(f"Failed to delete Workspace {workspace_id}: {unsuccessful_deletions[0]['ErrorMessage']}")
        else:
            print(f"Workspace {workspace_id} deletion initiated successfully.")
    except (BotoCoreError, ClientError) as error:
        print(f"An error occurred: {error}")
        raise

def delete_workspace_with_retries(workspace_id, max_retries=3, delay_seconds=10):
    """
    Delete a workspace with retries on failure.
    
    Parameters:
        workspace_id (str): The ID of the workspace to be deleted.
        max_retries (int): Maximum number of retries before giving up.
        delay_seconds (int): Delay between retries in seconds.
        
    Returns:
        None
    """
    attempts = 0
    while attempts < max_retries:
        try:
            print(f"Attempt {attempts+1} to delete Workspace {workspace_id}")
            delete_workspace(workspace_id)
            break
        except (BotoCoreError, ClientError) as error:
            print(f"Attempt {attempts+1} failed: {error}")
            attempts += 1
            if attempts < max_retries:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                print("Maximum retry attempts reached, failed to delete the workspace.")
                
# Example usage:
# Replace 'ws-12345678' with the actual Workspace ID
delete_workspace_with_retries('ws-12345678')
