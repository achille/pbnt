# Updated 2014 to work with Python 2.7 by Brandon Mikulka

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
#Major Packages
import sys
from numpy import *
#Library Packages
import ExampleModels as EX
sys.path.append('../lib')
from pbnt.Inference import *

def inferenceExample():
    """ This is an example of how to perform inference on a network using the Junction Tree Engine.  The exact same method could be used with any implemented inference engine by simply replaceing the line JunctionTreeEngine(water) with the appropriate constructor.
    """

    #define water network
    water = EX.water()

    #define variable indexes
    for node in water.nodes:
        if node.id == 0:
            cloudy = node
        if node.id == 1:
            sprinkler = node
        if node.id == 2:
            rain = node
        if node.id == 3:
            wetgrass = node
    #Create the inference engine object
    engine = JunctionTreeEngine(water)

    test0 = 1
    #Compute the marginal probability of sprinkler given no evidence
    Q = engine.marginal(sprinkler)[0]
    #Q is a DiscreteDistribution, and so to index into it, we have to use the class' method to create an index
    index = Q.generate_index([False], range(Q.nDims))
    print "The marginal probability of sprinkler=false:", Q[index]

    #Set cloudy and rain to False and True in the evidence
    engine.evidence[cloudy] = False
    engine.evidence[rain] = True
    #Compute the marginal probability given the evidence cloudy=False, rain=true
    Q = engine.marginal(wetgrass)[0]
    index = Q.generate_index([False],range(Q.nDims))
    print "The marginal probability of wetgrass=false | cloudy=False, rain=True:", Q[index]

#Run the inference example
inferenceExample()
