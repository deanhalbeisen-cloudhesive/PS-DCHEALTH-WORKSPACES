import boto3
from botocore.exceptions import BotoCoreError, ClientError
import time

# Initialize a session using your credentials
session = boto3.Session(
    # Optionally, you can specify your credentials and region here
    # aws_access_key_id='YOUR_KEY',
    # aws_secret_access_key='YOUR_SECRET',
    # region_name='YOUR_REGION'
)

# Create an S3 client
s3 = session.client('s3')

def list_s3_buckets_with_retry(max_retries=3, backoff_factor=1):
    """
    List all S3 buckets with details. This function includes a retry mechanism
    in case the request fails.

    Parameters:
        max_retries (int): Maximum number of retries if the request fails.
        backoff_factor (float): Factor by which to increase the delay between retries.

    Returns:
        list: A list of dictionaries containing bucket details.
    """
    retries = 0
    while retries < max_retries:
        try:
            # Make the API call to list buckets
            response = s3.list_buckets()
            buckets_details = []

            # Retrieve details for each bucket
            for bucket in response['Buckets']:
                # You can include more details by making additional API calls here
                bucket_details = s3.get_bucket_location(Bucket=bucket['Name'])
                bucket_details['Name'] = bucket['Name']
                bucket_details['CreationDate'] = bucket['CreationDate']
                buckets_details.append(bucket_details)

            return buckets_details

        except (BotoCoreError, ClientError) as error:
            print(f"An error occurred: {error}. Retrying...")
            time.sleep(backoff_factor * (2 ** retries))  # Exponential backoff
            retries += 1

    raise Exception("Max retries exceeded")

# Example usage:
if __name__ == "__main__":
    try:
        buckets = list_s3_buckets_with_retry()
        for bucket in buckets:
            print(bucket)
    except Exception as e:
        print(f"Failed to list buckets: {e}")
