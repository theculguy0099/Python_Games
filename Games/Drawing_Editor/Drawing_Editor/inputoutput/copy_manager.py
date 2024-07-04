class ClipBoardManager:
    def __init__(self):
        self._clipboard = None

    def copy(self, data):
        self._clipboard = data

    def paste(self):
        return self._clipboard

    def is_clipboard_empty(self):
        return self._clipboard is None
