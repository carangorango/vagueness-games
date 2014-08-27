#!/bin/bash

DATE=$(date +%Y%m%d-%H%M%S)
HEADER="Number of states,Prior distribution type,Number of messages,Impairment,Tolerance,Dynamics,Expected utility,Iterations"

echo $HEADER > results/$DATE.round_based.csv
for t in 10 50 90 130
do
    echo $t
    for i in 0 0.1 0.2 0.3 0.4 0.5
    do
        echo " $i"
    	for n in {1..20}
    	do
	        echo -n "  $n"
        	python vagueness-games_round_based.py $t 2 $i results/$DATE.round_based.csv
    	done
    	echo
    done
done
