import boto3
from botocore.exceptions import ClientError

def get_workspaces_details(max_retries=3):
    """
    Fetches details of all workspaces in the AWS account.

    Args:
    max_retries (int): Maximum number of retries for the API call in case of failure.

    Returns:
    list of dict: List of dictionaries where each dictionary contains details of a workspace.
    """

    # Initialize a session using your credentials
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',  # replace with your access key
        aws_secret_access_key='YOUR_SECRET_KEY',  # replace with your secret key
        region_name='YOUR_REGION'  # replace with your region
    )

    # Create an Amazon WorkSpaces client
    client = session.client('workspaces')

    # List to store all workspaces details
    workspaces_info = []

    try:
        # Initial API call to fetch workspaces
        response = client.describe_workspaces()

        # Collecting workspaces details
        workspaces_info.extend(response['Workspaces'])

        # Handling pagination if more workspaces are available
        while 'NextToken' in response:
            response = client.describe_workspaces(NextToken=response['NextToken'])
            workspaces_info.extend(response['Workspaces'])

    except ClientError as e:
        if max_retries > 0:
            print(f"API call failed, retrying... {max_retries} retries left")
            return get_workspaces_details(max_retries - 1)
        else:
            raise Exception("Max retries exceeded, failed to fetch workspaces details") from e

    return workspaces_info

# Example usage
if __name__ == "__main__":
    workspaces_details = get_workspaces_details()
    for workspace in workspaces_details:
        print(workspace)
