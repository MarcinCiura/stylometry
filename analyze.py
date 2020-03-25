#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import collections
import csv
import logging
import os
import re
import string
import unicodedata

def Unicode(text):
  return unicode(text, 'utf-8')

def Utf8(text):
  return text.encode('utf-8')

UPPERCASE_LETTERS = string.ascii_uppercase + 'ĄĆÉĘŁŃÓŚŹŻ'
LOWERCASE_LETTERS = string.ascii_lowercase + 'ąćéęłńóśźż'
CONVERT_TO_LOWERCASE = dict(zip(UPPERCASE_LETTERS, LOWERCASE_LETTERS))

def Lowercase(text):
  return ''.join([CONVERT_TO_LOWERCASE.get(x, x) for x in text])

ALPHANUMERIC = ''.join(
    unichr(x) for x in xrange(0x250)
    if unicodedata.category(unichr(x)) in ('Lu', 'Ll', 'Nd'))

Tokenize = re.compile(
    r'[{0}]+(?:-[{0}]+)*|[.,;:!?]+'.format(ALPHANUMERIC),
    re.MULTILINE | re.UNICODE).findall

# An assortment of frequent conjunctions,
# prepositions, adverbs, and qubliks.
INTERESTING_TOKENS = frozenset(u"""
    . ? ! ,
    a aby albo ale ani aż bo choć czy i jeśli lecz ni niech niż więc że żeby
    bez dla do ku jako na nad o od po pod przed przez przy u w we wkoło z ze za
    bardzo coraz dotąd dziś gdy jak kiedy kiedyś niegdyś nieraz nigdy potem
    razem sam stąd teraz tu tuż tyle tym tymczasem wnet wszystko wtem wtenczas
    się nie by co gdyby gdzie jakby jeszcze już ledwie może nawet niby
    przecież tak tam też to tylko właśnie zaraz znowu
""".split())


def Analyze(filename, writer):
  counter = collections.Counter()
  num_tokens = 0
  with open(filename) as f:
    contents = Unicode(f.read()).split(u'-----\r\nTa lektura,')[0]
    tokens = Tokenize(contents)
    author, _, title, subtitle = contents.splitlines()[:4]
    if subtitle:
      info = '%s: %s (%s)' % (author, title, subtitle)
    else:
      info = '%s: %s' % (author, title)
    logging.info('Processing %s: %s', filename, info)
    for token in tokens:
      num_tokens += 1
      token = Lowercase(token)
      if token in INTERESTING_TOKENS:
        counter[token] += 1
  writer.writerow(
      [filename, Utf8(info), num_tokens] +
      [counter[x] for x in sorted(INTERESTING_TOKENS)])

def main():
  logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
  dirname = 'txt'
  with open('texts.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['file', 'info', 'total'] +
        [Utf8(x) for x in sorted(INTERESTING_TOKENS)])
    for filename in os.listdir(dirname):
      Analyze(os.path.join(dirname, filename), writer)


if __name__ == '__main__':
  main()
