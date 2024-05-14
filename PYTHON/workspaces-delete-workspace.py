import boto3
from botocore.exceptions import ClientError
import time

# Configuration section
aws_region = 'your-region'  # Specify your AWS region
retry_attempts = 3  # Number of retries
wait_time = 10  # Wait time between retries in seconds

# Initialize AWS clients
client = boto3.client('workspaces', region_name=aws_region)

def delete_workspace(workspace_id):
    """
    Attempt to delete a single workspace given its ID.
    
    Args:
    workspace_id (str): The unique identifier for the workspace to delete.

    Returns:
    bool: True if deletion was successful, False otherwise.
    """
    try:
        response = client.terminate_workspaces(
            TerminateWorkspaceRequests=[
                {
                    'WorkspaceId': workspace_id
                },
            ]
        )
        # Check if the response was successful
        if response['FailedRequests']:
            print(f"Failed to delete workspace {workspace_id}: {response['FailedRequests'][0]['ErrorMessage']}")
            return False
        return True
    except ClientError as e:
        print(f"An error occurred: {e}")
        return False

def delete_workspaces_for_user(user_id):
    """
    Deletes all workspaces associated with a given user ID, with retries for failures.

    Args:
    user_id (str): The user ID whose workspaces are to be deleted.
    """
    try:
        # Describe workspaces filtered by user_id
        described = client.describe_workspaces(
            DirectoryId=user_id  # Assuming DirectoryId is used to filter by user ID
        )
        workspaces = described['Workspaces']

        for workspace in workspaces:
            attempts = 0
            success = False
            while attempts < retry_attempts and not success:
                success = delete_workspace(workspace['WorkspaceId'])
                if not success:
                    print(f"Retrying to delete workspace {workspace['WorkspaceId']} (Attempt {attempts+1}/{retry_attempts})")
                    time.sleep(wait_time)
                attempts += 1

            if not success:
                print(f"Failed to delete workspace {workspace['WorkspaceId']} after {retry_attempts} attempts.")

    except ClientError as e:
        print(f"An error occurred while trying to describe workspaces: {e}")

# Main execution
# Replace 'your-user-id' with the actual user ID
delete_workspaces_for_user('your-user-id')
