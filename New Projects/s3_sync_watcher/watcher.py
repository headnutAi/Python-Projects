from watchdog.events import FileSystemEventHandler

class UploadHandler(FileSystemEventHandler):
    def __init__(self, uploader, prefix):
        # TODO: letzte Upload-Zeitpunkte pro Datei speichern (für Debouncing)
        pass

    def on_created(self, event):
        pass

    def on_modified(self, event):
        # TODO: hier auch Debounce-Check + Filter für .tmp/~$ Dateien
        pass