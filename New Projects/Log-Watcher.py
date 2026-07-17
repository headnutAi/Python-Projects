from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import json, time
from datetime import datetime

class LogAlertHandler(FileSystemEventHandler):
    def __init__(self, alerts_file, patterns, debounce_seconds=5):

        self.alerts_file = alerts_file
        self.patterns = patterns
        self.debounce_seconds = debounce_seconds
        self.positions = {}
        self.last_alert_time = {}

        if Path(self.alerts_file).exists():
            with open(self.alerts_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = []

        pass

    def on_modified(self, event):
        if not event.is_directory:
            path = event.src_path
            print(path)

            if path.endswith(".log"):
                new_lines = self._read_new_lines(path)

                for new_line in new_lines:
                    if any(p in new_line for p in self.patterns):
                        if self._should_alert(path):
                            self._write_alert(path, new_line)

        pass

    def _read_new_lines(self, path):

        last_pos = self.positions.get(path, 0)

        if Path(path).stat().st_size < last_pos:
            last_pos = 0

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(last_pos)
            new_line = f.readlines()
            self.positions[path] = f.tell()
        return new_line



    def _should_alert(self, path):
        now = time.time()

        last = self.last_alert_time.get(path, 0)

        if now - last > self.debounce_seconds:
            self.last_alert_time[path] = now
            return True

        return False



    def _write_alert(self, filepath, line):
        timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        eintrag_neu = {"filepath" : filepath, "line" : line, "timestamp" : timestamp}

        self.data.append(eintrag_neu)

        with open(self.alerts_file, "w") as f:
            json.dump(self.data, f)

        pass


if __name__ == "__main__":
    watch_dir = "C:/Users/Headnut/Desktop/logs"
    handler = LogAlertHandler("alerts_file.json", ["ERROR", "CRITICAL"])
    observer = Observer()
    observer.schedule(handler, path=watch_dir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()