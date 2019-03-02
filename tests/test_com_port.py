from pyexpect import expect
from rewrite import com_port, com_port_init


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


def test_com_port_init():

    s = com_port_init(serial_obj=SerialMock())
    s.open()
    s.write(b'$KE,IO,SET,7,0\r\n')
    ans1 = s.read_all()
    s.write(b'$KE,WRA,000000010101010000000000\r\n')
    ans2 = s.read_all()

    expect(s.is_open).to_equal(True)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    s.close()

    expect(s.is_open).to_equal(False)


def test_com_port():
    s = com_port(serial_obj=SerialMock())

    s.open()
    s.write(b'$KE\r\n')

    expect(s.is_open).to_equal(True)
    expect(s.read_all()).to_equal(b'#OK\r\n')

    s.close()
    expect(s.is_open).to_equal(False)

