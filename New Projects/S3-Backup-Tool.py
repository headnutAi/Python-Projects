import argparse
import hashlib
import logging
from pathlib import Path
import time
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Ab welcher Dateigröße Multipart-Upload genutzt wird (Bytes)
MULTIPART_THRESHOLD = 100 * 1024 * 1024  # 100 MB
MAX_RETRIES = 3


def parse_args():
    parser = argparse.ArgumentParser(description="Sync lokaler Ordner -> S3 Bucket")

    parser.add_argument("bucket", help="S3 Bucket")
    parser.add_argument("local_dir", help="Local directory")
    parser.add_argument("--prefix", help="S3 Prefix", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def iter_local_files(local_dir: Path):
    for datei in local_dir.rglob("*"):
        if datei.is_file():
            if not datei.is_symlink():
                yield datei
            else:
                logger.warning("Symlink detected, skipping...")


def compute_md5(filepath: Path) -> str:
    hasher = hashlib.md5()

    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
        return hasher.hexdigest()


def get_remote_etag(s3_client, bucket: str, key: str) -> str | None:
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
        etag = response["ETag"]
        etag = etag.strip('"')

        return etag

    except ClientError as e:

        if e.response["Error"]["Code"] == "404":
            return None

        raise


def needs_upload(local_md5: str, remote_etag: str | None) -> bool:

    if remote_etag is None:
        return True
    elif "-" in remote_etag:
        return True
    elif remote_etag == local_md5:
        return False
    else:
        return True


def upload_with_retry(s3_client, filepath: Path, bucket: str, key: str, dry_run: bool):

    retries = 0
    config = TransferConfig(multipart_threshold=MULTIPART_THRESHOLD)

    if dry_run:
        logger.info(f"Dry run: {filepath}")
        return True
    else:

        while retries < MAX_RETRIES:
            try:
                s3_client.upload_file(filepath, bucket, key, Config=config)
                return True
            except ClientError as e:
                retries += 1
                time.sleep(2 ** retries)
                logger.info(f"Retry: {retries} / {MAX_RETRIES}")

        logger.info(f"Upload failed: {filepath}")
        return False

def main():
    args = parse_args()
    s3_client = boto3.client("s3")

    stats = {"uploaded": 0, "skipped": 0, "failed": 0}

    local_dir = Path(args.local_dir)


    for local_file in iter_local_files(local_dir):

        hash = compute_md5(filepath=local_file)
        etag_hash = get_remote_etag(s3_client, bucket=args.bucket, key=local_file.relative_to(local_dir).as_posix())

        if needs_upload(local_md5=hash, remote_etag=etag_hash):
            if upload_with_retry(s3_client, local_file, args.bucket, local_file.relative_to(local_dir).as_posix(), args.dry_run):
                stats["uploaded"] += 1
            else:
                stats["failed"] += 1

        else:
            stats["skipped"] += 1

    logger.info(
        "Fertig. Hochgeladen: %d, übersprungen: %d, fehlgeschlagen: %d",
        stats["uploaded"], stats["skipped"], stats["failed"],
    )


if __name__ == "__main__":
    main()
