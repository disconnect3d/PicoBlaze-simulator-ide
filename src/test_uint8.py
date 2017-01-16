from src.uint8 import uint8


def test_constructor1():
    assert int(uint8(20)) == 20


def test_constructor2():
    assert uint8(256) == uint8(0)
    assert uint8(260) == uint8(4)
    assert uint8(-1) == uint8(255)
    assert uint8(-5) == uint8(251)
    assert uint8(-5) != uint8(252)


def test_add_other():
    assert (uint8(50), 0) == uint8(20) + uint8(30)
    assert (uint8(5), 1) == uint8(250) + uint8(11)


def test_add_int():
    assert (uint8(50), 0) == uint8(20) + 30
    assert (uint8(5), 1) == uint8(250) + 11
    assert (uint8(251), 1) == uint8(1) + -6


def test_sub_other():
    assert (uint8(246), 1) == uint8(20) - uint8(30)
    assert (uint8(239), 0) == uint8(250) - uint8(11)


def test_sub_int():
    assert (uint8(246), 1) == uint8(20) - 30
    assert (uint8(239), 0) == uint8(250) - 11
    assert (uint8(7), 0) == uint8(1) - -6


def test_and_other():
    assert uint8(24) == uint8(31) & uint8(24)
    assert uint8(0) == uint8(17) & uint8(12)
    val = uint8(31)
    val &= uint8(24)
    assert val == uint8(24)


def test_and_int():
    assert uint8(24) == uint8(31) & 24
    assert uint8(0) == uint8(17) & 12
    val = uint8(31)
    val &= 24
    assert val == uint8(24)


def test_eq_int():
    assert uint8(42) == 42
    assert uint8(256) == 0
    assert uint8(-1) == 255


def test_mod():
    assert uint8(32) % 2 == 0
    assert uint8(5) % uint8(2) == 1


def test_lshift():
    assert (uint8(0), 1) == uint8(128) << 1
    assert (uint8(128), 1) == uint8(192) << 1
    assert (uint8(64), 0) == uint8(32) << 1


def test_getitem():
    assert uint8(16)[4] == 1
    assert uint8(16)[5] == 0
    for i in range(8):
        assert uint8(255)[i] == 1
        assert uint8(0)[i] == 0
