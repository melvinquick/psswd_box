import os


class QssFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def load_qss_file(self):
        with open(self.get_file_path(), "r") as f:
            return f.read()

    def get_file_path(self):
        return os.path.join(os.path.dirname(__file__), self.filename)
