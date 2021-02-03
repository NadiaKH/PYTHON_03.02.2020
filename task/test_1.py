import pytest
from .code import getUniqueNames, buildGraph, GraphIterator

def test_1():
    names = getUniqueNames('data')
    graph = dict(key_val for key_val in [(name, []) for name in names])
    buildGraph(graph, 'data')
    
    prev_g = None
    for g in GraphIterator(graph):
        if prev_g:
            assert prev_g[1] >= g[1]
        prev_g = g
