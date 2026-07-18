import argparse
import hashlib
import logging
from pathlib import Path

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
    """
    Upload mit Retry + exponentiellem Backoff.

    - Bei dry_run=True: nur loggen, kein echter Call.
    - Große Dateien (> MULTIPART_THRESHOLD) über TransferConfig.
    - Bei ClientError: bis zu MAX_RETRIES Versuche, mit steigender
      Wartezeit dazwischen (time.sleep(2 ** versuch)).
    - Nach MAX_RETRIES gescheiterten Versuchen: Fehler loggen und
      False zurückgeben (Skript soll NICHT abbrechen).

    Doku TransferConfig: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig
    Doku upload_file: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
    """
    # TODO
    raise NotImplementedError


def main():
    args = parse_args()
    s3_client = boto3.client("s3")

    stats = {"uploaded": 0, "skipped": 0, "failed": 0}

    # TODO: iter_local_files durchgehen
    #   -> relativen S3-Key bauen (local_dir-relativer Pfad + optionalem prefix)
    #   -> compute_md5
    #   -> get_remote_etag
    #   -> needs_upload prüfen
    #   -> ggf. upload_with_retry aufrufen
    #   -> stats hochzählen

    logger.info(
        "Fertig. Hochgeladen: %d, übersprungen: %d, fehlgeschlagen: %d",
        stats["uploaded"], stats["skipped"], stats["failed"],
    )


if __name__ == "__main__":
    main()
