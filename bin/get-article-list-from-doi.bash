#!/usr/bin/env bash
# get list of all articles in journal that the DOI on the command line is in
# usage: ./get-article-list-from-doii 10.1007/s10803-018-3803-7

# get the email address from the environment variable CROSSREF_EMAIL
if [ -z "$CROSSREF_EMAIL" ]; then
  echo "Please set the environment variable CROSSREF_EMAIL to your email address"
  exit 1
fi

DOI=$1
json=$(curl -s "https://api.crossref.org/works/$DOI?mailto=$CROSSREF_EMAIL")
# Two ISSNs for print and paper. the first one seems to work
ISSN=$(echo $json|jq -r .message.ISSN[0])
echo ISSN is $ISSN
journal=$(echo $json|jq -r '.message."short-container-title" |.[]')
SHORTNAME=$(echo "$journal" | awk '{for(i=1;i<=NF;i++) printf "%s", substr($i,1,1)}' | tr '[:upper:]' '[:lower:]')
echo Saving json list to $SHORTNAME.json
wget "https://api.crossref.org/journals/$ISSN/works?select=DOI,title,container-title,volume,issue,published&rows=1000&mailto=$CROSSREF_EMAIL" -O $SHORTNAME.json
echo Saving DOIs to $SHORTNAME-doi.txt
jq -r '.message.items[].DOI' < $SHORTNAME.json >$SHORTNAME-doi.txt
count=$(wc -l $SHORTNAME-doi.txt | xargs | cut -d ' ' -f 1)
echo Found $count articles in $journal
if [[ "$count" -ge 1000 ]]; then
  echo "More than 1000 articles in $journal.  Try a more specific DOI"
  echo try wget "https://api.crossref.org/journals/$ISSN/works?select=DOI,title,container-title,volume,issue,published&rows=1000&offset=1000&mailto=$CROSSREF_EMAIL" -O $SHORTNAME.json
  echo "A better solution would be to have this search also accept a year and get all items for the year, or range of years and save them as separate files"
fi
