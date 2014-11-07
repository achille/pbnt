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
from numpy import *
# Assume we are in dist/tests directory
sys.path.append('../lib')
# Library specific modules
from pbnt import Distribution
from pbnt import Node
from pbnt import Inference
from pbnt import Graph

class InferenceTestCase(unittest.TestCase):
    def setUp(self):
        cNode = Node.BayesNode(0, 2, name="cloudy")
        sNode = Node.BayesNode(1, 2, name="sprinkler")
        rNode = Node.BayesNode(2, 2, name="rain")
        wNode = Node.BayesNode(3, 2, name="wetgrass")

        #cloudy
        cNode.add_child(sNode)
        cNode.add_child(rNode)

        #sprinkler
        sNode.add_parent(cNode)
        sNode.add_child(wNode)

        #rain
        rNode.add_parent(cNode)
        rNode.add_child(wNode)

        #wetgrass
        wNode.add_parent(sNode)
        wNode.add_parent(rNode)

        self.nodes = [cNode, sNode, rNode, wNode]

        #create distributions
        #cloudy distribution
        cDistribution = Distribution.DiscreteDistribution(cNode)
        index = cDistribution.generate_index([],[])
        cDistribution[index] = 0.5
        cNode.set_dist(cDistribution)

        #sprinkler
        dist = zeros([cNode.size(),sNode.size()], dtype=float32)
        dist[0,] = 0.5
        dist[1,] = [0.9,0.1]
        sDistribution = Distribution.ConditionalDiscreteDistribution(nodes=[cNode, sNode], table=dist)
        sNode.set_dist(sDistribution)
        #rain
        dist = zeros([cNode.size(), rNode.size()], dtype=float32)
        dist[0,] = [0.8,0.2]
        dist[1,] = [0.2,0.8]
        rDistribution = Distribution.ConditionalDiscreteDistribution(nodes=[cNode, rNode], table=dist)
        rNode.set_dist(rDistribution)
        #wetgrass
        dist = zeros([sNode.size(), rNode.size(), wNode.size()], dtype=float32)
        dist[0,0,] = [1.0,0.0]
        dist[1,0,] = [0.1,0.9]
        dist[0,1,] = [0.1,0.9]
        dist[1,1,] = [0.01,0.99]
        wgDistribution = Distribution.ConditionalDiscreteDistribution(nodes=[sNode, rNode, wNode], table=dist)
        wNode.set_dist(wgDistribution)
        #create bayes net
        self.bnet = Graph.BayesNet(self.nodes)
        self.engine = Inference.InferenceEngine(self.bnet)

    def testBlankEvidence(self):
        nonEvidence = self.engine.evidence.empty()
        assert(set(nonEvidence) == set(self.nodes))

    def testInsertEvidence(self):
        node = self.nodes[2]
        self.engine.evidence[node] = 1
        nonEvidence = self.engine.evidence.empty()
        nodes = set([self.nodes[0], self.nodes[1], self.nodes[3]])
        assert(set(nonEvidence) == nodes)

suite = unittest.makeSuite(InferenceTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

if __name__ == "__main__":
    unittest.main()
