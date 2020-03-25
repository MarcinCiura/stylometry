#!/usr/bin/python

import collections
import csv
import sys

import numpy
import analyze

def Analyze(filename):
  counter = collections.Counter()
  num_tokens = 0
  with open(filename) as f:
    contents = analyze.Unicode(f.read())
    tokens = analyze.Tokenize(contents)
    for token in tokens:
      num_tokens += 1
      token = analyze.Lowercase(token)
      if token in analyze.INTERESTING_TOKENS:
        counter[token] += 1
  return num_tokens, [counter[x] for x in sorted(analyze.INTERESTING_TOKENS)]


def main():
  if len(sys.argv) < 2:
    sys.exit('Usage: %s filename' % sys.argv[0])
  titles = []
  data = []
  with open('texts.csv') as books:
    for line in csv.DictReader(books):
      titles.append(line['info'])
      total = float(line['total'])
      counts = {}
      for k, v in line.iteritems():
        if k in ('file', 'info', 'total'):
          continue
        counts[k] = v
      counts = sorted(counts.items())
      counts = numpy.array([float(x[1]) / total for x in counts])
      data.append(counts)

  num_tokens, counters = Analyze(sys.argv[1])
  this_point = numpy.array(counters) / float(num_tokens)
  distances = []
  for i in xrange(len(data)):
    distances.append(
        (numpy.linalg.norm(this_point - data[i]), titles[i]))
  distances.sort()
  for dist, title in distances[:5]:
    print dist, title


if __name__ == '__main__':
  main()
