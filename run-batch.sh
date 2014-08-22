#!/bin/bash

DATE=$(date +%Y%m%d-%H%M%S)
HEADER="Number of states,Prior distribution type,Number of messages,Impairment,Tolerance,Dynamics,Speaker entropy,Hearer entropy,Speaker convexity,Hearer convexity,Speaker Voronoiness,Hearer Voronoiness,Speaker informativity,Hearer informativity,Expected utility,Iterations,Speaker strategy file,Hearer strategy file"

echo $HEADER > results/$DATE.csv
for t in 10 50 90 130
do
    echo $t
    for i in 0 0.1 0.2 0.3 0.4 0.5
    do
        echo " $i"
    	for n in {1..100}
    	do
	        echo -n "  $n"
        	python vagueness-games.py $t 2 $i results/$DATE.csv
    	done
    	echo
    done
done
