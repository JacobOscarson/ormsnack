from _ast import *
import ast
from micropy import lang
from typing import Any, Callable, Collection, Iterable, Optional, Union

class NodeDesc: ...
AstAttrGetter = Callable[[], Any]
AstAttrSetter = Callable[[Any], None]
ExprGetter: Any
PrimOrDesc = Union[NodeDesc, Any]

class NodeDesc:
    full: ast.AST
    spec: Any
    ident: str
    get: AstAttrGetter
    set: AstAttrSetter
    hide: bool = ...
    getexpr: ExprGetter = ...
    @property
    def children(self) -> Collection[NodeDesc]: ...
    @property
    def value(self) -> Union[Union[NodeDesc, Collection[NodeDesc], Any]]: ...
    @value.setter
    def value(self, value: Any) -> None: ...
    @property
    def expr(self) -> Optional[ast.AST]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, idx: Any) -> Any: ...
    def __init__(self, full: Any, spec: Any, ident: Any, get: Any, set: Any, hide: Any, getexpr: Any) -> None: ...
N = NodeDesc

def astattrsetter(node: ast.AST, attrname: str) -> AstAttrSetter: ...
def astattrgetter(node: ast.AST, attrname: str) -> Union[AstAttrGetter, ExprGetter]: ...
def descend(*nodes: ast.AST) -> Iterable[NodeDesc]: ...
def descender(nodes: Iterable[ast.AST]) -> Iterable[NodeDesc]: ...

Native: Any
Described = Union[NodeDesc, Collection[NodeDesc]]
MaybeDesc: Any

class nodedisp(lang.callbytype):
    def __call__(self, native: Native) -> Described: ...

desc: nodedisp