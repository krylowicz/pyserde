from serde import serde
from serde.toml import to_toml, from_toml
from typing import Optional
import pytest


def toml_basics() -> None:
    @serde
    class Foo:
        v: Optional[int]

    f = Foo(10)
    assert "v = 10\n" == to_toml(f)
    assert f == from_toml(Foo, "v = 10\n")

    @serde
    class Bar:
        v: set[int]

    b = Bar({1, 2, 3})
    to_toml(b)


def test_skip_none() -> None:
    @serde
    class Foo:
        a: int
        b: Optional[int]

    f = Foo(10, 100)
    assert (
        to_toml(f)
        == """\
a = 10
b = 100
"""
    )

    f = Foo(10, None)
    assert (
        to_toml(f)
        == """\
a = 10
"""
    )


def test_skip_none_container_not_supported_yet() -> None:
    @serde
    class Foo:
        a: int
        b: list[Optional[int]]

    f = Foo(10, [100, None])
    with pytest.raises(TypeError):
        to_toml(f)
