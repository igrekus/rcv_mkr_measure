from pyexpect import expect
from rewrite import receiver_control
from serialmock import SerialMock


def test_receiver_control_with_bitstring_0_branch():

    s = SerialMock()

    ans = receiver_control(bit_str='0', state=0, serial_obj=s)

    expect(ans).to_equal('init complete')


def test_receiver_control_with_the_main_branch():
    s = SerialMock()

    ans1, ans2 = receiver_control(bit_str='bit6', state=0, serial_obj=s)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    ans1, ans2 = receiver_control(bit_str='bit5', state=0, serial_obj=s)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    ans1, ans2 = receiver_control(bit_str='bit4', state=1, serial_obj=s)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    ans1, ans2 = receiver_control(bit_str='bit3', state=1, serial_obj=s)
    expect(ans1).to_equal(b'#OK\r\n')
    expect(ans2).to_equal(b'#OK\r\n')

    s.close()
