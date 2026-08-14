import watchdog.events
from watchdog.events import FileSystemEventHandler
import logging
import os

class UploadHandler(FileSystemEventHandler):
    def __init__(self, uploader, prefix):
        self.uploader = uploader
        self.prefix = prefix
        self.last_event_time = {}
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

    def debounce_check(self, path, threshold = 1.0):

        currentTime = time.time()

        if path in self.last_event_time:
            temp = self.last_event_time[path]

            if currentTime - temp < threshold:
                self.last_event_time[path] = currentTime
                return True
            else:
                self.last_event_time[path] = currentTime
                return False
        else:
            self.last_event_time[path] = currentTime
            return False
    def on_created(self, event):

        filename = os.path.basename(event.src_path)

        if not event.is_directory:

            if self.should_ignore(event.src_path):
                logging.info("ignoring filtered {}".format(event.src_path))
                return
            if self.debounce_check(event.src_path):
                logging.info("ignoring debounce{}".format(event.src_path))
                return

            self.uploader.upload(event.src_path, self.prefix + filename)
            logging.info(f"File Created, {event.src_path}")

    def on_modified(self, event):

        filename = os.path.basename(event.src_path)

        if not event.is_directory:

            if self.should_ignore(event.src_path):
                logging.info("ignoring filtered{}".format(event.src_path))
                return
            if self.debounce_check(event.src_path):
                logging.info("ignoring debounced{}".format(event.src_path))
                return

            self.uploader.upload(event.src_path, self.prefix + filename)
            logging.info(f"File Modified, {event.src_path}")


        pass


