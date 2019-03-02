class SerialMock:

    def __init__(self, port='COM1', baudrate=115200, parity='N', bytesize=8, stopbits=1, timeout=0.2):
        self._port = port
        self._open = False
        self._last_write = b''
        self._success = b'#OK\r\n'

    def open(self):
        self._open = True

    def close(self):
        self._open = False

    def write(self, what):
        self._last_write = what

    def read_all(self):
        ans = b''
        if self._last_write == b'$KE\r\n':
            ans = self._success
        elif b'$KE,IO,SET,' in self._last_write:
            ans = self._success
        elif b'$KE,WRA,' in self._last_write:
            ans = self._success
        self._last_write = b''
        return ans

    @property
    def is_open(self):
        return self._open
