#!/bin/bash

rm table.csv
echo "tool stealing chameleon ranks threads lbfreq sections dmin dmax time min_abs_threshold" > table.csv

for f in 20191022_121607_results/*/*
do 
  python parse_samoa_log.py $f >> table.csv
done

for f in 20191002_133432_results/*/*
do
  python parse_samoa_log.py $f >> table.csv 
done

for f in 20191004_152043_results/*/*
do
  python parse_samoa_log.py $f >> table.csv 
done
