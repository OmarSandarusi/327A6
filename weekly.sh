#!/bin/bash
echo 'Starting weekly run'
for DAY in 1 2 3 4 5
do
	echo "Starting Day $DAY"
	./daily.sh $DAY
done
echo 'Done all 5 iterations of the week'