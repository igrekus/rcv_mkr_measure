class PnaMock:

    def __init__(self):
        self._last_write = ''
        self._success = '#OK'

    def write(self, what: str):
        self._last_write = what

    def read(self):
        ans = 0
        if self._last_write == 'SENS1:SWE:POINts?':
            ans = 401
        return ans

    def query(self, what: str):
        self.write(what)
        return self.read()

    def close(self):
        print('pna mock close')

