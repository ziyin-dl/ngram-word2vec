import argparse
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cPickle as pickle
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument('--folder', nargs='+',type = str, default = 'flowinfo')

accuracies = {}
args = parser.parse_args()
for folder in args.folder:
    this_starts = []
    this_ends = []
    for root, dirs, files in os.walk(folder):
         for file in files:
            if '.pkl' not in file:
                continue
            with open(os.path.join(root, file), "r") as f:
                key = int(file.split('.')[0].split('_')[-1])
                accuracies[key] = pickle.load(f)
x = []
y_by_test = defaultdict(list)
keys = sorted(accuracies.keys())
for k in keys:
    v = accuracies[k]
    print(v)
    x.append(k)
    for k1, v1 in v.iteritems():
      final_accuracy = v1[-1]
      y_by_test[k1].append(final_accuracy)

for k, y in y_by_test.iteritems():
  max_x = np.argmax(y)
  max_y = y[max_x]
  print('max for {} is {} at {}'.format(k, max_y, max_x))
  plt.plot(x, y)
  plt.title('Word2Vec Accuracy on Similarity ({})'.format(k))
  plt.xlabel('Dimensions')
  plt.ylabel('Accuracy')
  plt.savefig('{}/word2vec_similarity_{}.pdf'.format(folder, k))
  plt.close()



