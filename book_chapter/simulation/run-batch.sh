#!/bin/bash

for a in "0.0 1 0.05 1" "0.0 1 0.05 1 0.1 1"
do
    echo $a
    for b in "detached"
    do
        echo " $b"
        for n in {1..25}
        do
            echo -n "  $n "
            python vagueness-games.py --batch 30 1 0.05 $b $a
            if [ $? -ne 0 ]; then
                exit
            fi
        done
        echo
    done
done
