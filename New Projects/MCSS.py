import boto3
from pathlib import Path
import hashlib
import argparse
import concurrent.futures
import click
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@click.command()
@click.option('--source', required=True, help='Source to watch')
@click.option('--bucket', required=True, help='Buckets to watch')
@click.option('--workers', type=int, required=True, help='Number of workers')
@click.option('--prune', is_flag=True, help='Prune the buckets')


def main(source, bucket, workers, prune):

    files = []
    hashs = []
    data = {}



    def scan_local_file(source: Path) -> dict[str, str]:

        path = Path(source)

        for datei in path.rglob("*"):
            if datei.is_file():

                sha256_hash = hashlib.sha256()

                files.append(datei)

                with open(datei, "rb") as f:
                    while chunk := f.read(4096):
                        sha256_hash.update(chunk)

                    hashs.append(sha256_hash.hexdigest())

        for file, hash in zip(files, hashs):
            data[str(file)] = hash




if __name__ == '__main__':
    main()