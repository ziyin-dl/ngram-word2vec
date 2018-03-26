import subprocess
from termcolor import colored
import os
import cPickle as pickle
from read_credentials import readCredentials, ssh, scp

servers = readCredentials("good_hosts")

# stop training
# warning !! all python will be killed
processes = []
for server, user, passwd in servers:
    print('{} killall python'.format(ssh(server, user, passwd)))
    proc = subprocess.Popen('{} killall python'.format(ssh(server, user, passwd)), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed to kill running python scripts".format(server), 'red')
        print colored("Error: {}".format(err), 'red')
