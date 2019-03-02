from pyexpect import expect
from rewrite import receiver_control
from serialmock import SerialMock


def test_receiver_control_with_bitstring_0():

    s = SerialMock()

    ans = receiver_control(bit_str='0', state=0, serial_obj=s)

    expect(ans).to_equal('init complete')

