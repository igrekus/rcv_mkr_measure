from pyexpect import expect
from pnamock import PnaMock
from rewrite import pna_init


def test_init_pna():

    pna, err = pna_init(1, PnaMock())

    expect(isinstance(pna, PnaMock)).to_equal(True)
    expect(err).to_equal(0)

