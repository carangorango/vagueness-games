#!/bin/bash

DATE=$(date +%Y%m%d-%H%M%S)
HEADER="Number of states,Prior distribution type,Number of messages,Impairment,Tolerance,Dynamics,Expected utility,Iterations"

echo $HEADER > results/$DATE.round_based.csv
for t in 3 4 5 6 7
do
    echo $t
    for i in 0 0.025 0.05 0.075 0.1
    do
        echo " $i"
    	for n in {1..50}
    	do
	        echo -n "  $n"
        	python vagueness-games_round_based.py $t 2 $i results/$DATE.round_based.csv
    	done
    	echo
    done
done
