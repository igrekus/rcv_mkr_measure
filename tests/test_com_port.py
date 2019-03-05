from pyexpect import expect
from rewrite import com_port, jerome_init
from serialmock import SerialMock


def test_com_port_init():

    s = jerome_init(jerome=SerialMock())
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

