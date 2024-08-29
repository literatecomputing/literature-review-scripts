#!/usr/bin/env bash
# Get APA reference from DOI. Assumes that directory name is first part of DOI and the file name is the second part of DOI
# Abandoned: I would re-write to get DOI from the pdf file itself rather than the file and directory name
echo This probably does not work. It is a work in progress.
exit
header_file=$(mktemp)
# Function to get APA reference from DOI
get_apa_reference() {
    doi="$1"
    url="https://doi.org/$doi"
    apa_reference=$(curl -D $header_file -sLH "Accept: text/bibliography; style=apa" http://dx.doi.org/$doi)
    http_status=$(awk 'NR==1 {print $2}' "$header_file")

    # Check if the status code is 404
    if [ "$http_status" -eq 404 ]; then
      echo "The URL returned a 404 status code."
    else
      echo "The URL did not return a 404 status code. Status code: $http_status"
      cat $header_file
    fi

    echo $apa_reference
    sleep 10
}

for input_file in "."/*.pdf; do
  # Remove the ".pdf" extension from the filename
  base="${input_file%.pdf}"
  if [[ -f $base-apa.txt ]]
  then
    echo Have "$base-apa.txt"
    continue
  fi

  # get doi
  current_dir=$(basename "$PWD")
  if [[ $current_dir == 10.* ]]; then
    echo "current_dir starts with 10."
  else
    echo "current_dir does not start with 10. Skipping..."
    continue
  fi  
  doi=$current_dir/$base
  apa_reference=$(get_apa_reference $doi)

  echo "$base-apa.txt --->$apa_reference"
  echo "$apa_reference" > "$base-apa.txt"
  exit
done
