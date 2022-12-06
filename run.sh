#!/bin/bash

> data.tsv
python3 get_urls.py
python3 get_content.py &
pyscript_pid=$!

while true; do
    if [[ -s "data.tsv" ]]; then
        count_lines=$(cat "data.tsv" | wc -l)
        if [[ $count_lines -ge 20 ]]; then
            kill $pyscript_pid
            exit 0
        fi
    fi
done
