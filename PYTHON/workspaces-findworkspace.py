import boto3
import backoff
from botocore.exceptions import BotoCoreError, ClientError

# Initialize AWS client for WorkSpaces
client = boto3.client('workspaces')

@backoff.on_exception(backoff.expo,
                      (BotoCoreError, ClientError),
                      max_tries=5,
                      giveup=lambda e: e.response['Error']['Code'] == '403')
def get_user_id_from_workspace(workspace_id):
    """
    Retrieve the user ID associated with a given workspace ID.
    
    Args:
    workspace_id (str): The ID of the AWS Workspace.

    Returns:
    str: The user ID associated with the workspace.

    Raises:
    Exception: If the workspace ID is not found or API call fails after retries.
    """
    try:
        # Fetch the workspace information
        response = client.describe_workspaces(WorkspaceIds=[workspace_id])
        # Extract user ID from the response
        user_id = response['Workspaces'][0]['UserName']
        return user_id
    except IndexError:
        # Handle the case where the workspace does not exist or no user is found
        raise Exception("Workspace ID not found or no associated user.")
    except (BotoCoreError, ClientError) as error:
        # Additional handling can be done here (if needed)
        raise error

# Example usage
workspace_id = 'ws-1234567890abcdef0'
try:
    user_id = get_user_id_from_workspace(workspace_id)
    print(f"User ID: {user_id}")
except Exception as e:
    print(f"Failed to retrieve user ID: {e}")
