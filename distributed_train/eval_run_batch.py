import subprocess
from termcolor import colored
import os
from read_credentials import readCredentials

SSH, SCP, user = readCredentials("credentials.txt")

with open('good_hosts', 'r') as f:
    servers = [line.strip() for line in f.readlines()]

processes = []
for server in servers:
    proc = subprocess.Popen("{} eval_run.sh {}@{}:./word2vec/".format(SCP, user, server).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp script".format(server), 'red')

processes = []
for server in servers:
    proc = subprocess.Popen('{} {}@{} "cd word2vec;bash eval_run.sh"'.format(SSH, user, server), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to run script".format(server), 'red')
        print colored("Error: {}".format(output), 'red')

