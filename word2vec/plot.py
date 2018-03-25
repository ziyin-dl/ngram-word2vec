import argparse
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cPickle as pickle

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
y = []
max_x = 0
max_y = 0
keys = sorted(accuracies.keys())
for k in keys:
    v = accuracies[k]
    final_accuracy = v[-1]
    x.append(k)
    y.append(final_accuracy)
    if final_accuracy > max_y:
      max_y = final_accuracy
      max_x = k
plt.plot(x, y)
plt.title('Word2Vec Accuracy on Composability (Question Anser)')
plt.xlabel('Dimensions')
plt.ylabel('Accuracy')
plt.savefig('question_accuracy.png')
print('max is {} at {}'.format(max_y, max_x))

