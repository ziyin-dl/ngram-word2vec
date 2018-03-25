import subprocess
from termcolor import colored
import os
import argparse
import collections
import cPickle as pickle
from read_credentials import readCredentials

SSH, SCP = readCredentials("credentials.txt")

parser = argparse.ArgumentParser()
parser.add_argument("--num_workers", type=int, default=1)
parser.add_argument("--data_dir", type=str, default="../scripts/data/ngram_data")
parser.add_argument("--script_dir", type=str, default="../scripts")
parser.add_argument("--word2vec_dir", type=str, default="../word2vec")
parser.add_argument("--start", type=int, default=1800)
parser.add_argument("--end", type=int, default=2009)

args = parser.parse_args()


with open('good_hosts', 'r') as f:
    servers = [line.strip() for line in f.readlines()]
assert(len(servers) > 0)
# distribute files to good hosts
# only needs to distribute ngram data
processes = []
for server in servers:
    proc = subprocess.Popen('{} balaji@{} "rm -rf ngram;mkdir -p ngram/data;mkdir -p ngram/scripts"'.format(
        SSH, server), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to mkdir".format(server), 'red')
        print colored("Error: {}".format(output), 'red')

file_lists = collections.defaultdict(list)
lb = 0
for year in range(args.start, args.end):
    cur_server = servers[lb]
    file_lists[cur_server].append(os.path.join(args.data_dir, "{}-ngram.txt".format(year)))
    lb += 1
    if lb >= len(servers):
        lb = 0
with open("file_on_server.pkl", 'w') as f:
    pickle.dump(file_lists, f)

processes = []
for server in servers:
    print("copying {} to {}".format(file_lists[server], server))
    proc = subprocess.Popen("{} {} balaji@{}:ngram/data".format(SCP,
            " ".join(file_lists[server]), server).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, file, proc));

for server, file, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp {}".format(server, file), 'red')

processes = []
for server in servers:
    proc = subprocess.Popen("{} -r {} balaji@{}:ngram/".format(SCP,
        args.word2vec_dir, server).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp code".format(server), 'red')

processes = []
for server in servers:
    proc = subprocess.Popen("{} {}/* balaji@{}:ngram/scripts".format(SCP,
        args.script_dir, server), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print(colored("{} failed to scp scrpits".format(server), 'red'))
        print(err)

