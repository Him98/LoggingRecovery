#!/bin/bash 

if [ "$#" -eq 2 ]; then
    python3 20161120_1.py "$1" $2
fi
if [ "$#" -eq 1 ]; then
	python3 20161120_2.py "$1" 
fi
