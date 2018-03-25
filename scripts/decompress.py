import subprocess as sp
from os import listdir
from os.path import isfile, join
from multiprocessing import Queue, Process
import argparse


def decompress(queue, unzipped_dir):
  while not queue.empty():
    file = queue.get()
    print("decompressing {}".format(file))
    sp.check_output("unzip -o {} -d {}".format(file, unzipped_dir), shell=True)

parser = argparse.ArgumentParser()
parser.add_argument("--num_workers", type=int, default=10)
parser.add_argument("--download_dir", type=str, default="data/raw")
parser.add_argument("--unzip_dir", type=str, default="data/unzipped_data")

args = parser.parse_args()

num_files =  800
download_dir = args.download_dir
unzipped_dir = args.unzip_dir

files = [join(download_dir, f) for f in listdir(download_dir) if isfile(join(download_dir, f))]
assert(len(files) == num_files)
sp.check_output("mkdir -p {}".format(unzipped_dir), shell=True)

queue = Queue()
for file in files:
  queue.put(file)

workers = []
for i in range(args.num_workers):
  workers.append(Process(target=decompress, args=(queue, unzipped_dir)))

for worker in workers:
  worker.start()
for worker in workers:
  worker.join()
