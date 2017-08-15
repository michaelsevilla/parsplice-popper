#!/usr/bin/python
from collections import Counter

print "hello"

words = {}
i = 0
with open("parsplice.log", 'rw') as f:
  for line in f:
    for word in line.split():
      if word not in words:
        words[word] = 1
      else:
        words[word] += 1
    i += 1
    if i % 1000000 == 0:
      print str(i) + "... "

d = Counter(words)
print d.most_common(10)
