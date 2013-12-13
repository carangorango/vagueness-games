#!/bin/bash

DATE=$(date +%Y%m%d-%H%M)
HEADER="Number of states,Prior distribution type,Number of messages,Impairment,Tolerance,Dynamics,Speaker entropy,Hearer entropy,Speaker convexity,Hearer convexity,Speaker Voronoiness,Hearer Voronoiness,Expected utility,Iterations,Speaker strategy,Hearer strategy"

echo $HEADER > results-$DATE.csv
for t in 6 10 14 18 22
do
    echo $t
    for i in 0 0.05 0.1 0.15 0.2 0.25 0.3
    do
        echo " $i"
    	for n in {1..10}
    	do
	        echo "  $n"
        	python vagueness-games.py $t 2 $i results-$DATE.csv
    	done
    done
done
