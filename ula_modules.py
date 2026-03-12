#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b


    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]  # (1)

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    s = Signal(bool(0))
    half1 = halfAdder(x[0], y[0], soma[0], s)
    half2 = fullAdder(x[1], y[1], s, soma[1], carry)
    return instances()


@block
def adder(x, y, soma, carry):
    s = [Signal(bool(0)) for i in range(len(x) - 1)]
    hallist = [None for i in range(len(x))]
    hallist[0] = halfAdder(x[0], y[0], soma[0], s[0]),

    for e in range(1, len(x)- 1):
        hallist[e] = fullAdder(x[e], y[e], s[e-1], soma[e], s[e])
    hallist[-1] = fullAdder(x[-1], y[-1], s[-1], soma[-1], carry)
    return instances()

@block
def addervb(x, y, soma, carry):

    @always_comb
    def comb():
        total = int(x) + int(y)
        soma.next = total & ((1 << len(x)) - 1)
        carry.next = (total >> len(x)) & 1

    return instances()