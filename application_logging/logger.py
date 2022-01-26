from datetime import datetime

class AppLogger:
    def __init__(self, path):
        self.path = path
    def log(self, log_message):
        """
        This method allows you to your message in the given file_object
        """
        now = datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")
        f = open(self.path, 'a+')
        f.write(f"{date}/{current_time}\t\t{log_message}\n")
        f.close()
