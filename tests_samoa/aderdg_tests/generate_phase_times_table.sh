#!/bin/bash

rm table_long.csv
echo "tool stealing chameleon timeCCP ranks threads lbfreq sections dmin dmax time min_abs_threshold" > table_long.csv

for f in $WORK/aderdg_tests/long_aderdg*/*/*
do 
  echo $f
  python parse_samoa_log.py $f >> table_long.csv
done

