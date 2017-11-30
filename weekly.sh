#!/bin/bash
echo 'Starting weekly run...'
for DAY in 1 2 3 4 5
do
	echo "Starting Day $DAY"

	if [[ $DAY != 1 ]]; then
		# Move the previous days results into the input of this day
		PREV=$(($DAY - 1))
		cp "./outputs/day$PREV/newaccounts.txt" "./inputs/day$DAY/accounts.txt"
		cp "./outputs/day$PREV/newmasteraccounts.txt" "./inputs/day$DAY/masteraccounts.txt"
	fi

	./daily.sh $DAY
done
echo 'Done all 5 iterations of the week'