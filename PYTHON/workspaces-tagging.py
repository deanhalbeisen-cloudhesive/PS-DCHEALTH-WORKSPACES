import boto3
import backoff
from botocore.exceptions import ClientError

# Initialize a boto3 client for AWS WorkSpaces
client = boto3.client('workspaces')

# Function to apply tags to a workspace
def tag_workspace(workspace_id, tags):
    """
    Tags an AWS Workspace with a given set of tags.

    Parameters:
        workspace_id (str): The ID of the workspace to tag.
        tags (dict): A dictionary of tag keys and values to apply.

    Returns:
        response (dict): The response from the tag_resource API call.
    """
    try:
        response = client.create_tags(ResourceId=workspace_id, Tags=tags)
        return response
    except ClientError as error:
        raise  # Reraise the exception to be handled by the retry logic

# Backoff and retry strategy for handling retries when tagging fails
@backoff.on_exception(backoff.expo, ClientError, max_tries=8)
def tag_with_retry(workspace_id, tags):
    """
    Attempts to tag a workspace with a backoff and retry strategy
    in case of failures.

    Parameters:
        workspace_id (str): The ID of the workspace to tag.
        tags (dict): A dictionary of tag keys and values to apply.
    """
    return tag_workspace(workspace_id, tags)

# Example usage
workspace_id = 'ws-1234567890abcdef0'  # Example workspace ID
tags = {'Project': 'Development', 'Environment': 'Test'}

# Call the function with retry logic
try:
    result = tag_with_retry(workspace_id, tags)
    print("Tagging successful:", result)
except ClientError as error:
    print("Failed to tag the workspace:", error)
