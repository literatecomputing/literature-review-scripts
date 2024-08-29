#!/usr/bin/env bash
# chek if filename on input
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi
# return usage if -? or --help
if [ "$1" == "-?" ] || [ "$1" == "--help" ]; then
    echo "Script for extracting DOI from file. Looks for 'DOI: doi' in file."
    echo "Usage: $0 <filename>"
    exit 0
fi
# process all files in input
while [ -n "$1" ]; do
    if [ -f "$1" ]; then
        grep -e "^DOI: " $1 |cut -f 2 -d ' '
    else
        echo "File $1 not found."
    fi
    shift
done

