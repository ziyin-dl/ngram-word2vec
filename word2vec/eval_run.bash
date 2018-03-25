#!/bin/bash
for (( i=1; i < 100; ++i)); do
  echo "$((i*i))"
  python word2vec_eval.py --min_count 120 --embedding_size $((1*i)) --train_data=text8   --eval_data=word2vec/trunk/questions-words.txt   --save_path=./tmp/
done

for (( i=5; i < 50; ++i)); do
  echo "$((20*i))"
  python word2vec_eval.py --min_count 120 --embedding_size $((20*i)) --train_data=text8   --eval_data=word2vec/trunk/questions-words.txt   --save_path=./tmp/
done

for (( i=1; i < 11; ++i)); do
  echo "$((1000*i))"
  python word2vec_eval.py --min_count 120 --embedding_size $((1000*i)) --train_data=text8   --eval_data=word2vec/trunk/questions-words.txt   --save_path=./tmp/
done
