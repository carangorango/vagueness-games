#!/bin/bash

DATE=$(date +%Y%m%d-%H%M%S)
HEADER="Number of states,Prior distribution type,Number of messages,Impairment,Tolerance,Dynamics,Speaker entropy,Hearer entropy,Speaker convexity,Hearer convexity,Speaker Voronoiness,Hearer Voronoiness,Speaker informativity,Hearer informativity,Expected utility,Iterations,Speaker Convex Cat, Hearer Convex Cat, Speaker strategy file,Hearer strategy file"

echo $HEADER > results/$DATE.csv
for t in 6 10 50 90
do
    echo $t
    for i in 0 0.05 0.1 0.2 0.3
    do
        echo " $i"
	for p in 0.05 0.1 0.2 0.3
	do
	    echo -n "   $p"
    	    for n in {1..50}
    	    do
	        echo -n "    $n"
        	python vagueness-games.py $t 2 $i $p results/$DATE.csv
    	    done
	    echo
	done
    	echo
    done
done
