#! /usr/bin/env python

import getopt, sys
from numpy import *
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

try:
    from IPython import embed
except:
    pass

debug = False;

def main():
  #Import arguments and parse into options.
  try:
    optlist, remainder = getopt.getopt(sys.argv[1:], 'j:g:m:vh')
    #If no arguments profided
    if len(optlist) == 0:
      print "***Options required***"
      usage()
  #if inappropriate argument provided
  except getopt.GetoptError as err:
    print str(err)
    usage()

  for o, a in optlist:
    if o == "-v":
      debug = True
      if debug:
        #view input
        print "\nProvided Arguments: "
        print str(optlist) + "\n"
    elif o == "-h":
      usage()
    elif o == "-m":
      # Return the Marginal probability
      pass
    elif o == "-g":
      # Return the conditional probability
      pass
    elif o == "-j":
      # Return the joint probability
      pass

  #Initialize the Cancer Bayes Network
  # network = nGraph()
  #testing basic bayes net class implementation
  numberOfNodes = 4
  #name the nodes
  cloudy = 0
  sprinkler = 1
  rain = 2
  wetgrass = 3

  cNode = BayesNode(0, 2, name="cloudy")
  sNode = BayesNode(1, 2, name="sprinkler")
  rNode = BayesNode(2, 2, name="rain")
  wNode = BayesNode(3, 2, name="wetgrass")

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

  nodes = [cNode, sNode, rNode, wNode]

  #create distributions
  #cloudy distribution
  cDistribution = DiscreteDistribution(cNode)
  index = cDistribution.generate_index([],[])
  # embed()
  cDistribution[index] = 0.5
  cNode.set_dist(cDistribution)

  #sprinkler
  dist = zeros([cNode.size(),sNode.size()], dtype=float32)
  dist[0,] = 0.5
  dist[1,] = [0.9,0.1]
  sDistribution = ConditionalDiscreteDistribution(nodes=[cNode, sNode], table=dist)
  sNode.set_dist(sDistribution)

  #rain
  dist = zeros([cNode.size(), rNode.size()], dtype=float32)
  dist[0,] = [0.8,0.2]
  dist[1,] = [0.2,0.8]
  rDistribution = ConditionalDiscreteDistribution(nodes=[cNode, rNode], table=dist)
  rNode.set_dist(rDistribution)

  #wetgrass
  dist = zeros([sNode.size(), rNode.size(), wNode.size()], dtype=float32)
  dist[0,0,] = [1.0,0.0]
  dist[1,0,] = [0.1,0.9]
  dist[0,1,] = [0.1,0.9]
  dist[1,1,] = [0.01,0.99]
  wgDistribution = ConditionalDiscreteDistribution(nodes=[sNode, rNode, wNode], table=dist)
  wNode.set_dist(wgDistribution)


  #create bayes net
  water = BayesNet(nodes)
  for node in water.nodes:
    if node.id == 0:
      cloudy = node
    if node.id == 1:
      sprinkler = node
    if node.id == 2:
      rain = node
    if node.id == 3:
      wetgrass = node
  # embed()
  engine = JunctionTreeEngine(water)
  #Compute the marginal probability of sprinkler given no evidence
  Q = engine.marginal(cloudy)[0]
  # embed()
  index = Q.generate_index([True], range(Q.nDims))
  print "The marginal probability of Cloudy=true:", Q[index]

  # engine.evidence[cloudy] = True
  # #Compute the marginal probability given the evidence cloudy=False, rain=true
  # Q = engine.marginal(sprinkler)[0]
  # index = Q.generate_index([True],range(Q.nDims))
  # print "The marginal probability of wetgrass=false | cloudy=False, rain=True:", Q[index]

  #Run logic on bayes:


  #print result


def usage():
  print """
  Usage:
  ---
    Flags
    -g  conditional probablity
    -j  joint probability
    -m  marginal probability
    -v  verbose
    -h  help
  ---
    Input
    P  Polution   (p = low,  ~p = high)
    S  Smoker     (s = true, ~s = false)
    C  Cancer     (c = true, ~c = false)
    D  Dyspnoea   (d = true, ~d = false)
    X  X-Ray      (x = true, ~x = false)
  ---
    Example
    python bayesnet.py -jPSC
    (joint probabilities for Pollution, Smoker, and Cancer)

    python bayesnet.py -j~p~s~c
    (joint probability for pollution = h, smoker = f, cancer = f)

    python bayesnet.py -gc|s
    (conditional probability for cancer given that someone is a smoker)
  """
  sys.exit(2)

if __name__ == "__main__":
    main()
