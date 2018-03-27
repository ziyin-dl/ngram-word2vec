import subprocess
from termcolor import colored
import os
from read_credentials import readCredentials, ssh, scp

servers = readCredentials("good_hosts")

subprocess.check_output("mkdir -p data", shell=True)
processes = []
for server, user, passwd in servers:
    proc = subprocess.Popen(scp(server, user, passwd, "./data/", "~/ngram/word2vec/data/vector*", reverse=True).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed scp data".format(server), 'red')

subprocess.check_output("mkdir -p question_result_eval", shell=True)
processes = []
for server, user, passwd in servers:
    proc = subprocess.Popen(scp(server, user, passwd, "./question_result_eval/", "~/ngram/word2vec/question_result_eval/*", reverse=True).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed scp data".format(server), 'red')


subprocess.check_output("mkdir -p similarity_result_eval", shell=True)
processes = []
for server, user, passwd in servers:
    proc = subprocess.Popen(scp(server, user, passwd, "./similarity_result_eval/", "~/ngram/word2vec/similarity_result_eval/*", reverse=True).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append((server, proc));

for server, proc in processes:
    output, err = proc.communicate()
    if proc.returncode != 0:
        print colored("{} failed scp data".format(server), 'red')


