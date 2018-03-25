#!/bin/bash
# model training related
neg_samples=4
threads=12
dim=300

# which models to train
base_year=1901
year_inc=1

for (( i=0; i < 50; ++i)); do
  data=$(($base_year+$year_inc*$i))
  echo "$data"
  python word2vec_optimized.py --min_count 100 --num_neg_samples $neg_samples --concurrent_steps $threads --embedding_size $dim --train_data=/home/zyin/googlengram/scripts/data/ngram_data/"$data"-ngram.txt  --eval_data=word2vec/trunk/questions-words.txt   --save_path=./data/ #> output.log
done

