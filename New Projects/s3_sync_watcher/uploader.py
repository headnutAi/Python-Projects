import boto3
from botocore.exceptions import ClientError, NoCredentialsError

class S3Uploader:
    def __init__(self, bucket, dry_run=False):
        self.client = boto3.client('s3')
        # TODO

    def upload(self, local_path, key):
        # TODO: Retry-Loop mit Backoff (z.B. selbst schreiben oder Lib `tenacity` nutzen)
        # TODO: Exceptions abfangen: ClientError → error code prüfen (z.B. 'NoSuchBucket', 'AccessDenied')
        pass