## Get info from crossref

USER=$CROSSREF_UER \
JNL="TESOL%20Quarterly" \
VOL=44 \
ISSUE=1 \
PAGE=4 \
YEAR=2010 \
curl -s -L "https://doi.crossref.org/openurl?pid=$USER&title=$JNL&volume=$VOL&issue=$ISSUE&spage=$PAGE&date=$YEAR&redirect=false" | ./get-doi-from-xml

## Import add local files to Zotero

## List of DOI to publisher:

https://gist.github.com/TomDemeranville/8699224

## get-doi-from-crossref

pulls the DOI out of the XML from crossref

## MLJ RSS with reflexivity -- 40

https://onlinelibrary.wiley.com/action/showFeed?ui=120szr&mi=4jif66k&type=search&feed=rss&query=%2526content%253DarticlesChapters%2526dateRange%253D%25255B19800101%252BTO%252B20241231%25255D%2526field1%253DAllField%2526publication%253D15404781%2526target%253Ddefault%2526text1%253Dreflexivity

### run-all-pdf-to-text

run pdftotext on all pdf files in current directory

### rename-to-doi

looks for "To link to this article: " and expects https://doi.org/.... and then renames all txt and pdf files to the DOI.

Creates the directory.

Tried to use DOI: to find just the DOI, but sometimes DOI: came at the end of the line and the DOI was on the next line. This worked for the ones from TandF.

### getwileydoi

takes a DOI. Downloads the file using Wiley API. Must be run from on campus. Works only for journals that your library has a subscription for.

### all-tesol

./all-tesol

This file will got _all_ of tesol-journal since we couldn't find a reliable way to search the full text without downloading it.

And then I copied them all to tesj-backup. And then I deleted the ones that don't have the three words in them using delete-extra-tesj

Also a bunch of stuff that was retrieved from constellate that wasn't journal articles is in delete.txt. These were copied from the spreadsheet by hand, pasted into a file, and then I made a macro that made all of them be `rm`s.

all-mlj -- this will, I think, download all of mlj. But maybe it won't, and we don't need it to since we got the DOI list elsewhere.

get-all-tesq -- also unneeded, not sure if it works.

### get-wiley-dois

./get-wiley-dois

Status: Works!

Will download all wile journals the list that Constellate generated
that includes one of the WORDS from all Wiley journals from 5ca9272b-bed8-f648-4089-264539d883a0-sampled-metadata.csv
which Constellate claims is all of the ones with one of the THREE WORDS in the journals it knows about.

First it gets DOIs from wiley-dois.txt (john wiley... from constellate)

Seconds it gets DOIS from wiley2-tesol-quarterly.txt (just wiley constellate)

Also gets DOIS from tq-all-dois.txt. That file was generated from TQ_All3.txt that were downloaded from somewhere into a Endnote file that was exported to "all fields" (has lines like FIELDNAME: XXX, DOI: xxx).
