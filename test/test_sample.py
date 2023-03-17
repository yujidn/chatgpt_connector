import pytest

from python_repository_template import sample

odd_params = [(1, True), (2, False), (3, True), (5, True), (8, False), (13, True), (21, True), (34, False)]


@pytest.mark.parametrize("p", odd_params)
def test_odd(p):
    number, flg = p

    assert sample.is_odd(number) == flg
