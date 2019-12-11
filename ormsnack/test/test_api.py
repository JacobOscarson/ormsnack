# yapf

import pytest
from ormsnack import api
from typing import Any
import _ast
import codegen
from micropy import microscope as ms
from micropy import dig


def foo(x: Any) -> None:
    "Docstring"
    1
    2
    return x + 1


@pytest.fixture
def Fob() -> api.Snack:
    "Does Fn"
    return api.snacka(foo)


def fnbody(fob_) -> None:
    "Does fnboxy"
    return fob_.org.body[0].body[-1]


def test_snacka(Fob) -> None:
    "Should be able to roundtrip the example code."
    assert \
        type(compile(codegen.to_source(Fob.org), '', 'single')) == \
        type(foo.__code__)  # yapf: ignore


def test_simplify_return(Fob) -> None:
    "Should simplify_return"
    r_ = fnbody(Fob)
    ret = api.simplify(r_)
    # XXX
    assert ret.children[0].values == [('x', ), ('+', ), (1, )]


def test_snacka_simplified(Fob) -> None:
    "Should snacka_simplified"
    assert [el.value for el in Fob.rep.values[1:4]] == ['Docstring', 1, 2]
