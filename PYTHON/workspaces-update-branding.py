import boto3
from botocore.exceptions import BotoCoreError, ClientError
import time

# Constants for retries
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Initialize the boto3 client for WorkSpaces
client = boto3.client('workspaces')

def update_workspace_branding(workspace_id, branding_properties):
    """
    Updates the branding properties of a given Amazon WorkSpaces.

    Parameters:
        workspace_id (str): The ID of the workspace to update.
        branding_properties (dict): The branding properties to update.

    Returns:
        response (dict): The response from the AWS API.
    """
    for attempt in range(MAX_RETRIES):
        try:
            # Attempt to update the workspace branding
            response = client.modify_workspace_properties(
                WorkspaceId=workspace_id,
                WorkspaceProperties=branding_properties
            )
            return response
        except (BotoCoreError, ClientError) as error:
            print(f"Attempt {attempt + 1} failed with error: {error}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    workspace_id = 'ws-123456789'
    branding_properties = {
        'RunningMode': 'AUTO_STOP',  # Example property
        'RunningModeAutoStopTimeoutInMinutes': 60
    }
    try:
        update_result = update_workspace_branding(workspace_id, branding_properties)
        print("Update successful:", update_result)
    except Exception as error:
        print("Failed to update workspace branding:", error)
