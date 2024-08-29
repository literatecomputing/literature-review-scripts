# Stuff that might help you do a lit review

This is a collection of scripts that I used to download a bunch of articles to do a lit review. If you want to know how to download a bunch of articles that you do not have rights to download (presumably through an academic library that you have sanctioned access to) this likely will not help. If you do have access to journal articles though your library, this set of scripts might make it easier for you to download them without clicking in your web browser 4-20 times per article.

There's even a script to rename the PDFs so they make some sense.

The scripts that I think work are in `bin`. They were mostly used on a Linux box, but should work on a Mac. They probably work if you can use wsl under Windows, but I was unable to test that, in spite of eventually gaining access to a Windows box in order to be able to download over 2000 files from Taylor and Francis in just over half an hour. (If you want to do that, talk to your librarian; it requires that you do the work from a specific IP address that your librarian registers with T&F for a specific project and time period. If you need to download more than a couple hundred articles, contact your librarian as soon as you have a good enough description of your project that they can fill out the paperwork.)

For some journal we were unable to do a full-text search that I trusted to get a list of DOIs matching those keywords, so I downloaded the entire journal and then used Zotero to 

## Get info from crossref

USER=$CROSSREF_EMAIL \
JNL="TESOL%20Quarterly" \
VOL=44 \
ISSUE=1 \
PAGE=4 \
YEAR=2010 \
curl -s -L "https://doi.crossref.org/openurl?pid=$USER&title=$JNL&volume=$VOL&issue=$ISSUE&spage=$PAGE&date=$YEAR&redirect=false"

https://api.crossref.org/journals/09598138/works?query.title=Recent+Developments&select=DOI,title,volume,issue,created&rows=1000&mailto=$CROSSREF_EMAIL

USER=$CROSSREF_EMAIL \
JNL="International%20Multilingual%20Research%20Journal" \
VOL=10 \
ISSUE=1 \
YEAR=2016 \
curl -s -L "https://doi.crossref.org/openurl?pid=$USER&title=$JNL&volume=$VOL&issue=$ISSUE&date=$YEAR&redirect=false" |lless

https://api.crossref.org/journals/09598138/works?query.title=Recent+Developments&select=DOI,title,volume,issue,created&rows=1000&mailto=support@crossref.org

## Get full year of journal from Crossref

1931-3152

https://doi.crossref.org/openurl?pid=$CROSSREF_EMAIL&title=International%20Multilingual%20Research%20Journal&volume=10&issue=1&date=2016

## get-doi-from-crossref

pulls the DOI out of the XML from crossref

## MLJ RSS with reflexivity -- 40

https://onlinelibrary.wiley.com/action/showFeed?ui=120szr&mi=4jif66k&type=search&feed=rss&query=%2526content%253DarticlesChapters%2526dateRange%253D%25255B19800101%252BTO%252B20241231%25255D%2526field1%253DAllField%2526publication%253D15404781%2526target%253Ddefault%2526text1%253Dreflexivity

### how to get the text around a word

for x in \*txt; do grep -i positionality -A 10 -B 5 "$x"; echo "=========================" ; done |less

### run-all-pdf-to-text

run pdftotext on all pdf files in current directory

### rename-to-doi

looks for "To link to this article: " and expects https://doi.org/.... and then renames all txt and pdf files to the DOI.

Creates the directory.

Tried to use DOI: to find just the DOI, but sometimes DOI: came at the end of the line and the DOI was on the next line. This worked for the ones from TandF.

### getwileydoi

takes a DOI. Downloads the file using Wiley API. Must be run from on campus. Works only for journals that your library has a subscription for.
