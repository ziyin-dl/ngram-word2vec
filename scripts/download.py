import subprocess as sp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--download_dir", type=str, default="data/raw")

args = parser.parse_args()


num_files =  800

urls = ["http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-fiction-all-5gram-20090715-{}.csv.zip".format(i)
  for i in range(num_files)]

sp.check_output("mkdir -p {}", shell=True)

for url in urls:
  sp.check_output("wget -P {}/ {}".format(url), shell=True)

