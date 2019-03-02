from pyexpect import expect
from pnamock import PnaMock
from rewrite import init_pna


def test_init_pna():

    pna, err = init_pna(1)

    expect(pna).to_be(None)
    expect(err).to_equal(0)

