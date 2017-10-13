#!/bin/bash

for t in 6 10 50 90
do
    echo $t
    for i in 1 3 5 9
    do
        echo " $i"
        for p in 0.0 0.05 0.1
        do
            echo "   $p"
#                for n in {1..50}
#                do
#                echo -n "    $n"
            python vagueness-games.py --batch $t $i 0.05 $p
            if [ $? -ne 0 ]; then
                exit
            fi
#                done
        done
    done
done

for t in 6 10 50 90
do
    echo $t
    for i in 1 3 5 9
    do
        echo " $i"
        for p in 0.05 0.1
        do
            echo "   $p"
#                for n in {1..50}
#                do
#                echo -n "    $n"
            python vagueness-games.py --batch $t $i 0.05 0.0 $p
            if [ $? -ne 0 ]; then
                exit
            fi
#                done
        done
    done
done

for t in 6 10 50 90
do
    echo $t
    for i in 1 3 5 9
    do
        echo " $i"
#        for p in 0.0 0.05 0.1
#        do
#            echo -n "   $p"
#                for n in {1..50}
#                do
#                echo -n "    $n"
        python vagueness-games.py --batch $t $i 0.05 0.0 0.05 0.1
            if [ $? -ne 0 ]; then
                exit
            fi
#                done
#            echo
#        done
    done
done
