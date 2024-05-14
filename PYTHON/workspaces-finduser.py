import boto3
from botocore.exceptions import BotoCoreError, ClientError
import time

def get_workspace_ids(user_id, max_retries=3):
    """
    Retrieves workspace IDs for a given user ID with retries on failure.

    Parameters:
    - user_id (str): The user ID for which to retrieve workspace IDs.
    - max_retries (int): Maximum number of retries in case of API call failures.

    Returns:
    - list: A list of workspace IDs associated with the user ID.
    """
    client = boto3.client('workspaces')
    workspace_ids = []
    attempt = 0

    while attempt < max_retries:
        try:
            # Attempt to call the describe_workspaces API with filters based on user ID
            response = client.describe_workspaces(
                Filters=[
                    {
                        'Name': 'UserName',
                        'Values': [user_id]
                    }
                ]
            )

            # Extract workspace IDs from the response
            for workspace in response.get('Workspaces', []):
                workspace_ids.append(workspace['WorkspaceId'])
            
            # If workspaces are retrieved, break out of the loop
            if workspace_ids:
                break

        except (BotoCoreError, ClientError) as error:
            print(f"Attempt {attempt + 1} failed with error: {error}")
            attempt += 1
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            # Break out of the loop if the API call is successful
            break

    return workspace_ids

# Example usage:
user_id = "example_user_id"
workspaces = get_workspace_ids(user_id)
print("Workspace IDs:", workspaces)
