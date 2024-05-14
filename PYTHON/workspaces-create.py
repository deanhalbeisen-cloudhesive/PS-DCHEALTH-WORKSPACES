import boto3
from botocore.exceptions import ClientError
import time

# Initialize a boto3 client for Amazon WorkSpaces
client = boto3.client('workspaces')

def create_workspace(user_id, directory_id, bundle_id, kms_key_id):
    """
    Attempts to create a single Amazon Workspace for a specified user ID.

    :param user_id: The domain user ID for the WorkSpace.
    :param directory_id: The directory ID for the WorkSpace.
    :param bundle_id: The bundle ID for the WorkSpace.
    :param kms_key_id: The KMS key ID for encrypting the WorkSpace volumes.
    :return: The WorkSpace creation response.
    """
    try:
        response = client.create_workspaces(
            Workspaces=[
                {
                    'DirectoryId': directory_id,
                    'UserName': user_id,
                    'BundleId': bundle_id,
                    'UserVolumeEncryptionEnabled': True,
                    'RootVolumeEncryptionEnabled': True,
                    'VolumeEncryptionKey': kms_key_id
                }
            ]
        )
        return response
    except ClientError as e:
        return e

def create_workspaces_for_users(user_ids, directory_id, bundle_id, kms_key_id, retries=3):
    """
    Creates workspaces for a list of user IDs with retry logic.

    :param user_ids: List of user IDs.
    :param directory_id: The directory ID where the WorkSpaces should be created.
    :param bundle_id: The bundle ID to use for each WorkSpace.
    :param kms_key_id: The KMS key ID for volume encryption.
    :param retries: Number of retries in case of failures.
    """
    results = {}
    for user_id in user_ids:
        attempt = 0
        while attempt < retries:
            print(f"Attempting to create workspace for {user_id}, attempt {attempt + 1}")
            result = create_workspace(user_id, directory_id, bundle_id, kms_key_id)
            if 'FailedRequests' not in result:
                results[user_id] = 'Success'
                break
            else:
                print(f"Failed to create workspace for {user_id}: {result['FailedRequests'][0]['ErrorMessage']}")
                attempt += 1
                time.sleep(10)  # wait for 10 seconds before retrying
                results[user_id] = 'Failed after retries'
    return results

# Example usage:
user_ids = ['user1', 'user2']  # Domain user IDs
directory_id = 'd-1234567890'  # Directory ID for the WorkSpaces
bundle_id = 'wsb-abcdef123456'  # Bundle ID for the WorkSpaces
kms_key_id = 'alias/aws/workspaces'  # KMS key for encrypting volumes

# Call the function to create WorkSpaces
results = create_workspaces_for_users(user_ids, directory_id, bundle_id, kms_key_id)
print(results)
