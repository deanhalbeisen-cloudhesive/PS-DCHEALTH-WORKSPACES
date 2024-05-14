import boto3
from botocore.exceptions import ClientError
import time

# Initialize a boto3 client for EC2
ec2 = boto3.client('ec2')

def list_ec2_instances():
    """
    Lists all EC2 instances with their details. Implements retries in case of API call failures.
    """
    try:
        # Attempt to retrieve all EC2 instances
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)
        return instances
    except ClientError as e:
        print(f"Failed to fetch EC2 instances: {e}")
        return None

def retry_api_call(api_function, max_attempts=3, delay=5):
    """
    Retry wrapper for API calls.

    Args:
    api_function: The API function to call.
    max_attempts: Maximum number of attempts to try the API call.
    delay: Delay between retries in seconds.

    Returns:
    The result of the API function or None if all retries fail.
    """
    attempts = 0
    while attempts < max_attempts:
        result = api_function()
        if result is not None:
            return result
        attempts += 1
        print(f"Retrying... Attempt {attempts}")
        time.sleep(delay)
    print("Max retry attempts reached, exiting.")
    return None

# Use the retry wrapper to list EC2 instances
if __name__ == "__main__":
    ec2_instances = retry_api_call(list_ec2_instances)
    if ec2_instances:
        for instance in ec2_instances:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
    else:
        print("No instances could be retrieved.")
