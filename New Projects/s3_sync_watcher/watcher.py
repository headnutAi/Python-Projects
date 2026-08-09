import watchdog.events
from watchdog.events import FileSystemEventHandler
import logging
import os

class UploadHandler(FileSystemEventHandler):
    def __init__(self, uploader, prefix):
        self.uploader = uploader
        self.prefix = prefix
        # TODO: letzte Upload-Zeitpunkte pro Datei speichern (für Debouncing)
        pass

    def should_ignore(self, path):
        filename = os.path.basename(path)

        if filename.endswith(".tmp"):
            return True
        if filename.startswith("~$"):
            return True
        if filename.startswith("."):
            return True

        return False

    def on_created(self, event):
        if not event.is_directory:

            if self.should_ignore(event.src_path):
                logging.info("ignoring {}".format(event.src_path))
                return
            logging.info(f"File Created, {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:

            if self.should_ignore(event.src_path):
                logging.info("ignoring {}".format(event.src_path))
                return
            logging.info(f"File Modified, {event.src_path}")
        # TODO: hier auch Debounce-Check + Filter für .tmp/~$ Dateien
        pass


