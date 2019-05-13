from pyexpect import expect
from pnamkrmock import PnaMkrMock

def test_PnaMkrMock_create():

    mock = PnaMkrMock()

    expect(mock._success).to_equal("#OK")
