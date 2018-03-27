import subprocess
from termcolor import colored
import os
import argparse
import collections
import cPickle as pickle
from read_credentials import readCredentials, ssh, scp


parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", type=str, default="../scripts/data/ngram_data")
parser.add_argument("--word2vec_dir", type=str, default="../word2vec")
parser.add_argument("--start", type=int, default=1800)
parser.add_argument("--end", type=int, default=2009)
parser.add_argument("--clear_all", type=int, default=0)

args = parser.parse_args()


servers = readCredentials("good_hosts")
assert(len(servers) > 0)
# distribute files to good hosts
# only needs to distribute ngram data
if args.clear_all == 1:
    processes = []
    for server, user, passwd in servers:
        proc = subprocess.Popen('{} "rm -rf ngram;mkdir -p ngram/data;mkdir -p ngram/scripts"'.format(
            ssh(server, user, passwd)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append((server, proc));

    for server, proc in processes:
        output, err = proc.communicate()
        if proc.returncode != 0:
            print colored("{} failed to mkdir".format(server), 'red')
            print colored("Error: {}".format(output), 'red')

file_lists = collections.defaultdict(list)
lb = 0
for year in range(args.start, args.end):
    cur_server = servers[lb][0]
    file_lists[cur_server].append(os.path.join(args.data_dir, "{}-ngram.txt".format(year)))
    lb += 1
    if lb >= len(servers):
        lb = 0
with open("file_on_server.pkl", 'w') as f:
    pickle.dump(file_lists, f)

processes = []
for server, user, passwd in servers:
    print("copying {} to {}".format(file_lists[server], server))
    proc = subprocess.Popen(scp(server, user, passwd,
            " ".join(file_lists[server]), "ngram/data").split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, file, proc));

for server, file, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp {}".format(server, file), 'red')

processes = []
for server, user, passwd in servers:
    """scp(server, user, passwd, "{}/word2vec_eval.py".format(args.word2vec_dir), "ngram/word2vec/", recursive=False)"""
    cmd = scp(server, user, passwd, args.word2vec_dir, "ngram/", recursive=True)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp code".format(server), 'red')
        print(err)
