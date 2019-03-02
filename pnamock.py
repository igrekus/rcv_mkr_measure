class PnaMock:

    def __init__(self):
        self._last_write = ''
        self._success = '#OK'

    def write(self, what: str):
        self._last_write = what

    def read(self):
        return self._last_write

    def query(self, what: str):
        self.write(what)
        return self.read()

