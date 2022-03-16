#!/bin/bash
python tests/unit/test_example.py 2> result.txt
RESULT=$(cat result.txt | grep "OK")
if [[ "$RESULT" == "OK" ]]; then
    echo -e "Test OK.\n"
    exit 0
else
    echo -e "Run Unit Test Failed.\n"
    echo -e "Output: $(cat result.txt)\n"
    exit 1
fi