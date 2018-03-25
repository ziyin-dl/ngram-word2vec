import subprocess as sp
from os import listdir, linesep, walk
from os.path import isfile, join
from multiprocessing import Queue, Process
import argparse
import string
import collections
import cPickle as pickle

def process(queue, tmp_dir, out_dir):
  while not queue.empty():
    year = str(queue.get())
    ngram_by_year = ""
    onegram_by_year = collections.Counter()
    frequent_words = set()
    total_count = 0
    print("processing year {}".format(year))
    for root, subdirs, files in walk(tmp_dir):
      for filename in files:
        file = join(root, filename)
        if year not in file or ".txt" not in file:
          continue
        # print("processing {}".format(file))
        with open(file, 'r') as f:
          for line in f:
            ngram_by_year += line.lower()
            total_count += 1
    print("total {} ngrams".format(total_count))
    with open(out_dir + "/" + str(year) + "-ngram.txt", 'w') as f:
      f.write(ngram_by_year)
    """ okay, seems we can deal with frequency count in the training phase. No need for the 1gram counts"""
    """
    # now, deal with 1-grams
    for root, subdirs, files in walk(tmp_dir):
      for filename in files:
        file = join(root, filename)
        if year not in file or ".pkl" not in file:
          continue
        # print("processing {}".format(file))
        with open(file, 'r') as f:
          onegram_sub = pickle.load(f)
        for k, v in onegram_sub.iteritems():
          key = k.lower()
          onegram_by_year[key] += v
          if onegram_by_year[key] > 100:
            if key not in frequent_words:
              frequent_words.add(key)

    print("{} words for year {}, {} with occurrence > 100".format(sum(onegram_by_year.values()), year, len(frequent_words)))
    print("most common: {}".format(onegram_by_year.most_common()[:10]))

    # sp.check_output("rm {}".format(file), shell=True)
    with open(out_dir + "/" + str(year) + "-onegram.pkl", 'w') as f:
      pickle.dump(onegram_by_year, f)
    """

parser = argparse.ArgumentParser()
parser.add_argument("--num_workers", type=int, default=1)
parser.add_argument("--tmp_dir", type=str, default="data/tmp_processed_data")
parser.add_argument("--out_dir", type=str, default="data/ngram_data")
parser.add_argument("--start", type=int, default=1800)
parser.add_argument("--end", type=int, default=2009)
parser.add_argument("--inc", type=int, default=1)

args = parser.parse_args()

out_dir = args.out_dir
tmp_dir = args.tmp_dir

sp.check_output("mkdir -p {}".format(out_dir), shell=True)
queue = Queue()
years = range(args.start, args.end + 1, args.inc)
for year in years:
  queue.put(year)

workers = []
for i in range(args.num_workers):
  workers.append(Process(target=process, args=(queue, tmp_dir, out_dir)))

for worker in workers:
  worker.start()
for worker in workers:
  worker.join()
