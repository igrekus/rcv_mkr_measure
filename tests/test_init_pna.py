from pyexpect import expect
from pnamock import PnaMock
from rewrite import init_pna


def test_init_pna():

    pna, err = init_pna(1, PnaMock())

    expect(isinstance(pna, PnaMock)).to_equal(True)
    expect(err).to_equal(0)

