# --------------------
class MockLogger:
    # --------------------
    def __init__(self):
        self._lines = []

    # --------------------
    def clear(self):
        self._lines = []

    # --------------------
    def info(self, msg):
        print(f'INFO {msg}')
        self._lines.append(msg)
