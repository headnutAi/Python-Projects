import watchdog.events
from watchdog.events import FileSystemEventHandler
import logging

class UploadHandler(FileSystemEventHandler):
    def __init__(self, uploader, prefix):
        self.uploader = uploader
        self.prefix = prefix
        # TODO: letzte Upload-Zeitpunkte pro Datei speichern (für Debouncing)
        pass

    def on_created(self, event):
        if not event.is_directory:

            logging.info(f"File Created, {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File Modified, {event.src_path}")
        # TODO: hier auch Debounce-Check + Filter für .tmp/~$ Dateien
        pass