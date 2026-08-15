# cli.py
from uploader import S3Uploader
from watcher import UploadHandler
from watchdog.observers import Observer
import logging
import click

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@click.command()
@click.option('--folder', required=True, help='Folder to watch')
@click.option('--bucket', required=True, help='Bucket to watch')
@click.option('--prefix', required=True, help='Prefix to use')
@click.option('--dry-run', is_flag=True, default=False, help='dry run')


def main(folder, bucket, prefix, dry_run):
    logger = logging.getLogger()


    logger.info(f'Starting upload watcher mit den werten: {folder, bucket, prefix, dry_run}')

    uploader = S3Uploader(bucket, dry_run=dry_run)
    handler = UploadHandler(uploader, prefix)

    observer = Observer()
    observer.schedule(handler, folder, recursive=False)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()



if __name__ == "__main__":
    main()