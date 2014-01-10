# This file had been modified to implement task 1, i.e., normalize
# words that were rare.
# It will put the original word count to a file called 'word_count', then
# replace all words that is rare in the training data to '_RARE_'. All counts
# it output, a.k.a the model trained will be based on the normalized data.

#! /usr/bin/python

__author__="Alexander Rush <srush@csail.mit.edu>"
__date__ ="$Sep 12, 2012"

import sys, json

"""
Count rule frequencies in a binarized CFG.
"""

class Counts:
  def __init__(self):
    self.unary = {}
    self.binary = {}
    self.nonterm = {}
    self.word_count = {}

  def show(self):
    for symbol, count in self.nonterm.iteritems():
      print count, "NONTERMINAL", symbol

    for (sym, word), count in self.unary.iteritems():
      print count, "UNARYRULE", sym, word

    for (sym, y1, y2), count in self.binary.iteritems():
      print count, "BINARYRULE", sym, y1, y2

    with open('word_count', 'w') as out:
      for word, count in self.word_count.iteritems():
        out.write("%s %d\n" % (word, count))

  def reset_rules(self):
    self.unary = {}
    self.binary = {}
    self.nonterm = {}

  def count(self, tree, replace_rare):
    """
    Count the frequencies of non-terminals and rules in the tree.
    """
    if isinstance(tree, basestring): return

    # Count the non-terminal symbol. 
    symbol = tree[0]
    self.nonterm.setdefault(symbol, 0)
    self.nonterm[symbol] += 1
    
    if len(tree) == 3:
      # It is a binary rule.
      y1, y2 = (tree[1][0], tree[2][0])
      key = (symbol, y1, y2)
      self.binary.setdefault(key, 0)
      self.binary[(symbol, y1, y2)] += 1
      
      # Recursively count the children.
      self.count(tree[1], replace_rare)
      self.count(tree[2], replace_rare)
    elif len(tree) == 2:
      # It is a unary rule.
      y1 = tree[1]
      if replace_rare and self.word_count[y1] < 5:
        y1 = '_RARE_'
      key = (symbol, y1)
      self.unary.setdefault(key, 0)
      self.unary[key] += 1

      if not replace_rare:
        self.word_count.setdefault(y1, 0)
        self.word_count[y1] += 1

def main(parse_file):
  counter = Counts() 
  for l in open(parse_file):
    t = json.loads(l)
    counter.count(t, replace_rare = False)

  counter.reset_rules()
  
  for l in open(parse_file):
    t = json.loads(l)
    counter.count(t, replace_rare = True)
  counter.show()

def usage():
    sys.stderr.write("""
    Usage: python count_cfg_freq.py [tree_file]
        Print the counts of a corpus of trees.\n""")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    usage()
  else:
    main(sys.argv[1])
  
