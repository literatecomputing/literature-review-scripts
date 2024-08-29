#!/usr/bin/env bash
# Extract DOI from pdf files
# Assumes first page of PDF includes "DOI: the-doi-number". It tries to deal with spurious newlines and slashes in the first page.
# works for (recent?) Wiley and Taylor & Francis
# mostly the same code as normalize-filename, which may be more up to date
if [[ $# -eq 0 ]]; then
  echo "Usage: $0 file1.pdf file2.pdf ..."
  exit 1
fi
get_doi_from_pdf_file() {
  local pdf="$1"
  # pdftotext: get first page of PDF
  # tr: replace newlines with spaces (sometimes a newline will break the between DOI: and DOI or break DOI into two lines)
  # sed: replace slash-space with slash (sometimes the DOI is split at the slash which we replaced with a space)
  # grep: get the line with the DOI (but that's the whole thing?
  # awk: split the line at DOI:, leaving the DOI and the rest of the line
  # awk: get just the first word (the DOI)
  pdftotext "$pdf" -l 1  -  |tr '\n' ' ' | sed 's|/ |/|' | grep DOI:| awk -F 'DOI: ' '{print $2}' | awk '{print $1}'
}
if [[ $# -eq 1 ]]; then
  # for single file, just print the DOI
  pdf="$1"
  doi=$(get_doi_from_pdf_file "$pdf")
  echo "$doi"
  exit 1
fi
for pdf in "$@"; do
  # for multiple files, print the DOI and the filename
  doi=$(get_doi_from_pdf_file "$pdf")
  echo "$doi: $pdf"
done

