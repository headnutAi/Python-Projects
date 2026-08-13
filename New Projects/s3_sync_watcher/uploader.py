import boto3
import logging
import time
from botocore.exceptions import ClientError, NoCredentialsError

class S3Uploader:
    def __init__(self, bucket, dry_run=False):
        self.client = boto3.client('s3')
        self.bucket = bucket
        self.dry_run = dry_run

    def upload(self, local_path, key):

        if self.dry_run:
            logging.info('Dry run, skipping upload')
            return None
        max_retries = 4
        wait_seconds = 1

        for i in range(max_retries):
            try:
                response = self.client.upload_file(local_path, self.bucket, key)
                logging.info('Uploaded %s to S3 bucket: %s', key, response['Key'])
                return True

            except NoCredentialsError as c:
                logging.info('No credentials found, stopping')
                raise ValueError("No credentials found")

            except ClientError as e:
                error_code = e.response['Error']['Code']

                if error_code == 'AccessDenied' or error_code == 'NoSuchBucket':
                    raise ValueError('Access Denied or NoSuchBucket stopping...')
                else:
                    time.sleep(wait_seconds)
                    wait_seconds *= 2

        logging.info(f"Upload after{max_retries} retries failed")
        pass