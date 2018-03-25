import subprocess as sp
from os import listdir, linesep
from os.path import isfile, join
from multiprocessing import Queue, Process
import argparse
import string
import collections
import cPickle as pickle

def process(queue, tmp_dir, years):
  years_lookup = set(map(str, years))
  while not queue.empty():
    file = queue.get()
    ngram_by_year = {}
    onegram_by_year = {}
    for year in years:
      ngram_by_year[str(year)] = []  # strings of "ngram\t count"
      onegram_by_year[str(year)] = collections.Counter()   # token: count
    print("processing {}".format(file))
    out_of_year_count = 0
    total_count = 0
    with open(file, 'r') as f:
      for line in f:
        row = line.strip().split("\t")
        if (len(row) < 5):
          print(line)
          continue
        filtered = row[0].translate(None, string.punctuation)
        filtered = filtered.decode('unicode_escape').encode('ascii','ignore')
        ngram = filtered.strip().split(" ")
        year = row[1]
        total_count += 1
        if year not in years_lookup:
          out_of_year_count += 1
          continue
        match_count = row[2]
        # update onegrams: this is an approx. but is close
        for token in ngram:
          onegram_by_year[year][token] += int(match_count)
        ngram_by_year[year].append("\t".join([filtered, match_count]))
        # print(ngram)
    print("total {} ngrams with {} out of year range".format(total_count, out_of_year_count))
    out_dir = "{}/{}".format(tmp_dir, file.split('/')[-1])
    sp.check_output("mkdir -p {}".format(out_dir), shell=True)
    for year in years:
      with open(out_dir + "/" + str(year) + "-onegram.pkl", 'w') as f:
        pickle.dump(onegram_by_year[str(year)], f)
      with open(out_dir + "/" + str(year) + "-ngram.txt", 'w') as f:
        f.write(linesep.join(ngram_by_year[str(year)]))
    sp.check_output("rm {}".format(file), shell=True)

parser = argparse.ArgumentParser()
parser.add_argument("--num_workers", type=int, default=1)
parser.add_argument("--unzip_dir", type=str, default="data/unzipped_data")
parser.add_argument("--tmp_dir", type=str, default="data/tmp_processed_data")
parser.add_argument("--start", type=int, default=1800)
parser.add_argument("--end", type=int, default=2009)

args = parser.parse_args()

num_files =  800
unzipped_dir = args.unzip_dir
tmp_dir = args.tmp_dir

files = [join(unzipped_dir, f) for f in listdir(unzipped_dir) if isfile(join(unzipped_dir, f))]
assert(len(files) == num_files)
sp.check_output("mkdir -p {}".format(tmp_dir), shell=True)

queue = Queue()
for file in files:
  queue.put(file)

workers = []
years = range(args.start, args.end + 1)
for i in range(args.num_workers):
  workers.append(Process(target=process, args=(queue, tmp_dir, years)))

for worker in workers:
  worker.start()
for worker in workers:
  worker.join()
