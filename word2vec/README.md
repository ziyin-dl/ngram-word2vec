This is a skip-gram Word2Vec model that trains on ngram data. It is modified from the
original tensorflow word2vec kernel, but the input takes a ngram file. Each line of the ngram input file
is tab("\t") seperated, where the first part is the ngram, and the second part is the number of occurrences.
The ngram file does not have to be of all the same size. It's valid, for example, to have mixed 3-grams and
5-grams. A sample input file is

### ngram.txt
```
a quick brown \t 1
fox jumps the lazy yellow \t 2
blue cloud and white \t 5
```

A sample usage can be found
[here](run.sh).

This directory contains models for unsupervised training of word embeddings
using the model described in:

(Mikolov, et. al.) [Efficient Estimation of Word Representations in Vector Space](http://arxiv.org/abs/1301.3781),
ICLR 2013.

Detailed instructions on how to get started and use them are available in the
tutorials. Brief instructions are below.

* [Word2Vec Tutorial](http://tensorflow.org/tutorials/word2vec)

You can get the google ngram data using scripts in ./scripts

You will need to compile the ops as follows:

```shell
TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')
TF_LIB=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_lib())')
g++ -std=c++11 -shared word2vec_ops.cc word2vec_kernels.cc -o word2vec_ops.so -fPIC -I $TF_INC -O2 -D_GLIBCXX_USE_CXX11_ABI=0 -L$TF_LIB -ltensorflow_framework
```

Here is a short overview of what is in this directory.

File | What's in it?
--- | ---
`word2vec.py` | A version of word2vec implemented using TensorFlow ops and minibatching.
`word2vec_test.py` | Integration test for word2vec.
`word2vec_optimized.py` | A version of word2vec implemented using C ops that does no minibatching.
`word2vec_optimized_test.py` | Integration test for word2vec_optimized.
`word2vec_kernels.cc` | Kernels for the custom input and training ops.
`word2vec_ops.cc` | The declarations of the custom ops.
