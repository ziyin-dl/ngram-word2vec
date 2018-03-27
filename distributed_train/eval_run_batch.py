import subprocess
from termcolor import colored
import os
import cPickle as pickle
from read_credentials import readCredentials, ssh, scp


servers = readCredentials("good_hosts")
server_list = [x[0] for x in servers]
with open('file_on_server.pkl', 'r') as f:
    server_files = pickle.load(f)

for server, files in server_files.iteritems():
    if server in server_list:
        server_files[server] = [x.split('/')[-1] for x in files]

# note the params (min_count, data, etc) should match the train scripts
server_bash_scripts = {}
bash_script = """#!/bin/bash
trap "exit" INT
dim=300
declare -a ngram_files=({})
for data in "${{ngram_files[@]}}"; do
  echo "$data"
  python word2vec_eval.py --min_count 100 --embedding_size $dim --train_data="$data" --eval_data=word2vec/trunk/questions-words.txt   --save_path=./data/
done"""
for server, files in server_files.iteritems():
    server_bash_scripts[server] = bash_script.format(' '.join(['"../data/{}"'.format(x) for x in files]))

processes = []
for server, user, passwd in servers:
    with open('tmpbash_{}'.format(server), 'w') as f:
        f.write(server_bash_scripts[server])
        proc = subprocess.Popen(scp(server, user, passwd, "tmpbash_{}".format(server), "~/ngram/word2vec/run_eval.sh").split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp script".format(server), 'red')

subprocess.check_output("rm tmpbash_*", shell=True)
# start evaluating

processes = []
for server, user, passwd in servers:
    proc = subprocess.Popen('{} "cd ./ngram/word2vec;bash run_eval.sh"'.format(ssh(server, user, passwd)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to run script".format(server), 'red')
        print colored("Error: {}".format(output), 'red')

