### distributed train

This directory contains scripts for training large amount of embeddings on different servers. We use
the Google ngram data as an example, where the ngram files are processed and produced for each year. 
We will train word embeddings for every year between 1800 and 2009, so there will be 209 models to be 
trained. It will be helpful to distribute the job on different machines.

Here is a short overview of what is in this directory.

Directory | What's in it?
--- | ---
`good_hosts` | The config file containing the server credentials. Each line is comma separated, with the form "hostname, username, password"
`cp_data_batch.py` | Moving data to the servers. If you have n servers, each will get m/n ngram files where m is the number of ngram corpora.
`train_batch.py` | Start training on all the servers
`stop_training_batch.py` | Stop training on all the servers (by performing killall python jobs, use with caution)
