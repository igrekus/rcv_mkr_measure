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

    serial_obj = com_port_init(serial_obj=SerialMock())
    serial_obj.open()
    serial_obj.write(b'$KE,IO,SET,7,0\r\n')
    ans1 = serial_obj.read_all()
    serial_obj.write(b'$KE,WRA,000000010101010000000000\r\n')
    ans2 = serial_obj.read_all()

    expect(serial_obj.is_open).to_equal(True)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    serial_obj.close()

    expect(serial_obj.is_open).to_equal(False)

