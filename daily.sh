#!/bin/bash
ORIGDIR=`pwd`

# Run all tests in input/output directories
cd input
for feature in `ls -v`
do
echo "Testing feature: $feature"
    cd $feature
    for test in `ls -v`
    do
        echo "Running test: $test"
        TESTDIR="$ORIGDIR/input/$feature/$test"
        OUTDIR="$ORIGDIR/output/$feature/$test"
        python "$ORIGDIR/main.py" "$TESTDIR/accounts.txt" "$OUTDIR/transactions.txt" \
            < "$TESTDIR/input.txt" > "$OUTDIR/log.txt"
    done
    cd ../
    echo ""
done

# Run the comparison on each test result
cd ../
passed=0
failed=0
for feature in `ls -v output`
do
    echo "Comparing test results for $feature"
    for test in `ls -v output/$feature`
    do
        # Check first that the test is actually supposed to output a file
        if [ -f expected/$feature/$test/transactions.txt ]; then
            # Check if the output is the same as the expected output
            OUTPUT="output/$feature/$test/transactions.txt"
            EXPECT="expected/$feature/$test/transactions.txt"

            # Check and make sure the test output a file, as it was supposed to
            if [ -f output/$feature/$test/transactions.txt ]; then
                diff -q --strip-trailing-cr $OUTPUT $EXPECT>/dev/null
                EXITCODE=$?
                if [ $EXITCODE -ne 0 ]; then
                    RES="Test failed - difference detected in output."
                    ((failed++))
                else
                    RES="Test passed."
                    ((passed++))
                fi
            else
                RES="Test failed - it did not generate an output file."
                ((failed++))
            fi
        else
            # Check that the test run also didn't create the file
            if [ -f output/$feature/$test/transactions.txt ]; then
                RES="Test failed - it was not supposed to generate an output file."
                ((failed++))
            else
                RES="Test passed."
                ((passed++))
            fi
        fi
        printf "%-35s - %10s\n" $test "$RES"
    done
    echo ""
done

echo "Tests passed: $passed --- Tests failed: $failed"
