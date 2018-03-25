# ngram-word2vec

This is a skip-gram Word2Vec model that trains on ngram data. Unlike the original implementation, 
which takes a corpus as input, this implementation takes a n-gram file instead. Minimum changes were
made to the original Google implementation

* [Word2Vec Tutorial](http://tensorflow.org/tutorials/word2vec)

whose model is described in:

(Mikolov, et. al.) [Efficient Estimation of Word Representations in Vector Space](http://arxiv.org/abs/1301.3781),
ICLR 2013.

n-grams are co-occurrences of words in a corpus. For example, given a sentence "the quick brown fox jumps over the lazy dog",
the 5-grams contained are

5-gram | counts
--- | ---
`the quick brown fox jumps` | 1
`quick brown fox jumps over` | 1
`brown fox jumps over the` | 1
`fox jumps over the lazy` | 1
`jumps over the lazy dog` | 1

The ngram file is tab separated. The first part is the ngram itself, and second is its count. It's allowed that
the input file contains mixed ngrams. It's possible to put 3-grams and 5-grams together in one input file. We also
included an example on how to use this on the Google ngram dataset

* [Google Books Ngram](https://books.google.com/ngrams)

![Google Ngram](ngram.JPG?raw=true "Google Ngram")

Here is a short overview of what is in this directory.

Directory | What's in it?
--- | ---
`scripts` | The scripts for getting and processing the Google Ngram data.
`distributed_train` | Training Word2Vec models on multiple machines (if you have)
`word2vec` | The source code of the ngram word2vec, modified from Tensorflow source codes
