import subprocess
from termcolor import colored
import os
import cPickle as pickle
import argparse
from read_credentials import readCredentials, ssh, scp



parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, default=1800)
parser.add_argument("--end", type=int, default=2009)

args = parser.parse_args()


servers = readCredentials("good_hosts")
with open('file_on_server.pkl', 'r') as f:
    server_files = pickle.load(f)

for server, files in server_files.iteritems():
    server_files[server] = [x.split('/')[-1] for x in files
            if args.start <= int(x.split('/')[-1].split('-')[0]) and args.end >= int(x.split('/')[-1].split('-')[0])]

server_bash_scripts = {}
bash_script = """#!/bin/bash
trap "exit" INT
# model training related
neg_samples=4
threads=8
dim=300

rm -rf train_log
mkdir train_log
# which models to train
declare -a ngram_files=({})
for data in "${{ngram_files[@]}}"; do
  echo "$data"
  python word2vec_optimized.py --min_count 100 --num_neg_samples $neg_samples --concurrent_steps $threads --embedding_size $dim --train_data=../data/"$data"  --eval_data=word2vec/trunk/questions-words.txt   --save_path=./data/ > ./train_log/"$data"-output.log
done"""
for server, files in server_files.iteritems():
    server_bash_scripts[server] = bash_script.format(' '.join(['"../data/{}"'.format(x) for x in files]))

processes = []
for server, user, passwd in servers:
    with open('tmpbash_{}'.format(server), 'w') as f:
        f.write(server_bash_scripts[server])
    proc = subprocess.popen(scp(server, user, passwd, "tmpbash_{}".format(server), "./ngram/word2vec/run.sh").split(), stdout=subprocess.pipe, stderr=subprocess.pipe)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp script".format(server), 'red')

subprocess.check_output("rm tmpbash_*", shell=true)
# start training
processes = []
for server, user, passwd in servers:
    proc = subprocess.Popen('{} "cd ./ngram/word2vec;bash run.sh"'.format(ssh(server, user, passwd)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to run script".format(server), 'red')
        print colored("Error: {}".format(output), 'red')

