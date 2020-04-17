#!/bin/bash

rm table.csv
echo "tool stealing chameleon timeCCP ranks threads lbfreq sections dmin dmax time min_abs_threshold" > table.csv

for f in $WORK/aderdg_tests/aderdg*/*/*
do 
  echo $f
  python parse_samoa_log.py $f >> table.csv
done

