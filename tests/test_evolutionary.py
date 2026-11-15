import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from game_theory.evolutionary import step, path


def test_first_no_fee_step():
    assert abs(step(0.5, 0) - 0.48125) < 1e-12


def test_share_stays_in_unit_interval():
    for fee in (0, 2):
        assert all(0 <= x <= 1 for x in path(fee))
