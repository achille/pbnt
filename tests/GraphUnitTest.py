# PBNT: Python Bayes Network Toolbox
#
# Copyright (c) 2005, Elliot Cohen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * The name "Elliot Cohen" may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/env python
# Builtin Python Libraries
import sys
import unittest
# Major Packages
import numpy
# Assume we are in dist/tests directory
sys.path.append('../lib')
# Library specific modules
from pbnt import Distribution
from pbnt import Node
from pbnt import Graph
from pbnt.GraphExceptions import *

class TopoSortTestCase(unittest.TestCase):
    def setUp(self):
        a = Node.DirectedNode(1)
        b = Node.DirectedNode(2)
        c = Node.DirectedNode(3)
        d = Node.DirectedNode(4)
        e = Node.DirectedNode(5)

        a.add_child(b)
        a.add_child(c)
        b.add_parent(a)
        c.add_parent(a)
        d.add_child(b)
        b.add_parent(d)
        e.add_child(a)
        a.add_parent(e)

        self.nodes = [a,b,c,d,e]

    def testBasicSetIndex(self):
        """ Test that indices are correct relative to each other, using very basic network structure
        """
        self.graph = Graph.DAG(self.nodes)
        assert(self.nodes[0].index > self.nodes[4].index and \
               self.nodes[1].index > self.nodes[0].index and \
               self.nodes[1].index > self.nodes[3].index and \
               self.nodes[2].index > self.nodes[0].index), \
              "Indexes were not set properly in DAG.topological_sort()"

    def testAllIndexSet(self):
        """ Test that all indices are >= 0
        """
        self.graph = Graph.DAG(self.nodes)
        for node in self.nodes:
            assert(node.index >= 0), "Index was less than 0"

    # def testRaiseCyclicException(self):
    #     """ Test that the cyclic graph raises an exception.
    #     """
    #     self.nodes[0].add_child(self.nodes[4])
    #     self.nodes[4].add_parent(self.nodes[0])
    #     self.assertRaises(BadGraphStructure, Graph.DAG, self.nodes)

suite = unittest.makeSuite(TopoSortTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

if __name__ == "__main__":
    unittest.main()
