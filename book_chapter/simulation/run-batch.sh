#!/bin/bash

for a in "0.0 0.1 0.05 0.9" "0.0 0.2 0.05 0.8" "0.0 0.3 0.05 0.7" "0.0 0.4 0.05 0.6" "0.0 0.5 0.05 0.5" "0.0 0.6 0.05 0.4" "0.0 0.7 0.05 0.3" "0.0 0.8 0.05 0.2" "0.0 0.9 0.05 0.1"
do
    for n in {1..25}
    do
        echo -n "  $n "
        python vagueness-games.py --batch 30 1 0.05 weakest $a
        if [ $? -ne 0 ]; then
            exit
        fi
    done
done
echo
