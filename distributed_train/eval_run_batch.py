import subprocess
from termcolor import colored
import os

SSH = 'sshpass -p bala123 ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
SCP = 'sshpass -p bala123 scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

with open('good_hosts', 'r') as f:
    servers = [line.strip() for line in f.readlines()]

processes = []
for server in servers:
    proc = subprocess.Popen("{} eval_run.sh balaji@{}:./word2vec/".format(SCP, server).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to scp script".format(server), 'red')

processes = []
for server in servers:
    proc = subprocess.Popen('{} balaji@{} "cd word2vec;bash eval_run.sh"'.format(SSH, server), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to run script".format(server), 'red')
        print colored("Error: {}".format(output), 'red')

