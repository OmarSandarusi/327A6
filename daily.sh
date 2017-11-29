#!/bin/bash

# Expects the day to be the first command line options passed to the file

ORIGDIR=`pwd`
NUMSESSIONS=3
DAY="day$1"
NEXTDAY=$(($1 + 1))
INDIR="$ORIGDIR/inputs/$DAY"
OUTDIR="$ORIGDIR/outputs/$DAY"


# Run each session of the front end for the given day
cd input
for i in `seq $NUMSESSIONS`
do
echo "Running session $i on $DAY..."
        python "$ORIGDIR/src/frontend/main.py" "$INDIR/accounts.txt" "$OUTDIR/transaction$i.txt" \
            < "$INDIR/session$i.txt" > "$OUTDIR/session$i.log"
done

# Combine the transaction files produced by these sessions
# into a merged transaction file
echo "Merging transaction files..."
rm "$OUTDIR/mergedtransactions.txt"

for j in `seq $NUMSESSIONS`
do
    echo "`cat "$OUTDIR/transaction$j.txt"`" >> "$OUTDIR/mergedtransactions.txt"
done
echo "EOS 0000000 000 0000000 ***" >> "$OUTDIR/mergedtransactions.txt"
echo "Done."

# Run the backoffice on this new transaction file
echo "Running backoffice for $DAY..."
python "$ORIGDIR/src/backend/backend.py" "$OUTDIR/mergedtransactions.txt" "$INDIR/masteraccounts.txt" "$OUTDIR/newmasteraccounts.txt" "$OUTDIR/newaccounts.txt"
echo "Done."