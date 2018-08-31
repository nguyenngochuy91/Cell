#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import networkx as nx

g=nx.DiGraph()
g.add_edges_from([(1,2123123123), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9),
                  (4,10), (5,11), (5,12), (6,13)])
p=nx.drawing.nx_pydot.to_pydot(g)
p.write_png('example.png')