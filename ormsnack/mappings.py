# yapf

from _ast import *
import ast
from kingston import lang
from kingston import match

from typing import Any, Iterable, Callable, Optional, Union, Collection, cast
from dataclasses import dataclass
import funcy

from . import desc as desc_module

from .desc import (NodeDesc, nodedisp, AstAttrGetter, AstAttrSetter,
                   ExprGetter, PrimOrDesc, astattrgetter, astattrsetter,
                   descender)

N = NodeDesc
snap = desc_module.NodeState

desc: nodedisp = nodedisp({  # hm? starting out by just descending into it..
    # XXX irregularity:
    ast.BinOp:
    lambda bo: [desc(bo.left), desc(bo.op),
                desc(bo.right)],
    ast.Expr:
    lambda expr: desc(expr.value),
    ast.If:
    lambda iff: N(state=lambda cur=iff: snap(full=cur,
                                             spec='if',
                                             ident='if',
                                             value=[desc(n) for n in cur.body],
                                             expr=cur.test),
                  ident='if',
                  get=lambda: [desc(n) for n in iff.body],
                  set=astattrsetter(iff, 'body'),
                  getexpr=astattrgetter(iff, 'test')),
    ast.Call:
    lambda call: N(state=lambda cur=call: snap(full=cur,
                                               spec=f'call/{cur.func.id}',
                                               ident=dn.func.id,
                                               value=cur.func,
                                               expr=()),
                   ident=call.func.id,
                   get=astattrgetter(call, 'func'),
                   set=astattrsetter(call, 'func')),
    ast.FunctionDef:
    lambda fdef: N(state=lambda cur=fdef: snap(
        full=cur,
        spec='def',
        ident=cur.name,
        value=[desc(child) for child in cur.body],
        expr=cur.args),
                   ident=fdef.name,
                   get=astattrgetter(fdef, 'body'),
                   set=astattrsetter(fdef, 'body'),
                   getexpr=astattrgetter(fdef, 'args')),
    ast.arguments:
    lambda args: N(state=lambda cur=args: snap(
        full=cur,
        spec='args',
        ident='({})'.format(','.join(arg.arg for arg in args.args)),
        value=cur.args,
        expr=()),
                   ident='({})'.format(','.join(arg.arg for arg in args.args)),
                   get=astattrgetter(args, 'args'),
                   set=astattrsetter(args, 'args')),
    ast.arg:
    lambda arg: N(
        state=lambda cur=arg: snap(
            full=cur, spec='arg', ident=cur.arg, value=cur.arg, expr=()),
        ident=arg.arg,
        get=astattrgetter(arg, 'arg'),
        set=astattrsetter(arg, 'arg'),
    ),
    ast.Compare:
    lambda cmp_: N(state=lambda cur=cmp_: snap(
        full=cur,
        spec='cmp',
        ident='cmp',
        value=descender([cur.left, *cur.comparators]),
        expr=()),
                   ident='cmp',
                   get=descender([cmp_.left, *cmp_.comparators]),
                   set=astattrsetter(cmp_, 'comparators')),
    ast.Str:
    lambda s: N(state=lambda cur=s: snap(
        full=cur, spec=str, ident=s.s, value=s.s, expr=()),
                ident=s.s,
                get=astattrgetter(s, 's'),
                set=astattrsetter(s, 's')),
    ast.Num:
    lambda num: N(state=lambda cur=num: snap(
        full=cur, spec=type(cur.n), ident=str(cur.n), value=cur.n, expr=()),
                  ident=str(num.n),
                  get=astattrgetter(num, 'n'),
                  set=astattrsetter(num, 'n')),
    ast.Add:
    lambda a: N(state=lambda cur=a: snap(
        full=cur, spec='op/+', ident='+', value='+', expr=()),
                ident='+',
                get=lambda: '+',
                set=astattrsetter(a, 'op')),
    ast.Return:
    lambda ret: N(state=lambda cur=ret: snap(full=cur,
                                             spec='return',
                                             ident='return',
                                             value=desc(cur.value),
                                             expr=cur.value),
                  ident='return',
                  getexpr=astattrgetter(ret, 'value'),
                  get=astattrgetter(ret, 'value'),
                  set=astattrsetter(ret, 'value')),
    ast.Constant:
    lambda con: N(state=lambda cur=con: snap(full=cur,
                                             spec=type(cur.value),
                                             ident=str(cur.value),
                                             value=cur.value,
                                             expr=()),
                  ident=str(con.value),
                  get=astattrgetter(con, 'value'),
                  set=astattrsetter(con, 'value')),
    ast.Name:
    lambda name: N(state=lambda cur=name: snap(
        full=cur, spec=cur.id, ident=cur.id, value=cur.id, expr=()),
                   ident=name.id,
                   get=astattrgetter(name, 'id'),
                   set=astattrsetter(name, 'id'))
})

desc_module.desc = desc

p2a: match.Match = match.Match({
    str: lambda v: ast.Name(id=v),
})
