## See below for doing lit review stuff, but the most useful part of this is renaming a PDF to a normalized name of author, year, and title.

`normalize-filename` and `pdf-make-bibliography` both run on a Mac and can be made a "quick action". The script attempts to fix the
path and let you know if something is missing and how to fix it.

If you are someone who is good with a Mac and could make these instructions better, I would appreciate knowing how to fix them.
I've done it twice now, but failed to make very good notes.

This is sort-of what to do.

You need homebrew, pdftotex, and for the bibliography, JabRef and TeX package . First, install https://brew.sh

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install poppler
```

I think that's all that's required for the rename script.

Crossref likes you to provide a real email address in exchange for giving you the DOI data for free. Or they used to. Now I can't find
anywhere that says that.

To run it from the command line, you'll do something like this:

```
git clone https://github.com/literatecomputing/literature-review-scripts/
export CROSSREF_EMAIL='you@youremai.com'
bin/normalize-filename Downloads/some-pdf-that-is-an-article.pdf
```

For the normalize-filename script, you should see out put something like this:

```
 ./literature-review-scripts/bin/normalize-filename ./Downloads/19313152.2014.852426.pdf
/home/pfaffman/Downloads/19313152.2014.852426.pdf -- Getting https://api.crossref.org/works/10.1080/19313152.2014.852426?mailto=jay@literatecomputing.com
Renaming: /home/pfaffman/Downloads/19313152.2014.852426.pdf -> /home/pfaffman/Downloads/Macedo 2014 - Multiculturalism Permitted in English Only.pdf
```

There are other formats that right now require modifying [the script](https://github.com/literatecomputing/literature-review-scripts/blob/main/bin/normalize-filename#L156-L168). Here are some examples:

```
  author_year_jnl="$year-$author-$short_j"
  author_year_abbr_title="$year-$author-$abbr_title"
  author_year_title="$author$year$short_title"
  year_author_jnl_doi="$year-$author-$short_j-$FILE_DOI"
  year_author_title_spaces="$year $author $short_title_spaces"
  author_year_title_spaces="$author $year - $short_title_spaces"

  # choose the one you like and make it be the target_filename

  target_filename="$author_year_title_spaces"
  target_path="$ITEM_DIR/$target_filename.pdf"
```

For the Bibliography generator, you need also MacTeX and JabRef. JabRef is a Normal Mac Program you can get the `dmg` from their [installation page](](https://github.com/jabref/jabref/releases/tag).

```
brew install --cask mactex
```

Create a Quick Action that runs a script and works for PDF files. It should pass the names as arguments (not as input to the script)

Put something like this in the place that it seems like it should go:

```
#!/bin/bash

# Set environment variables
export PATH="/Users/YOURUSER/literature-review-scripts/bin":/opt/homebrew/bin:$PATH
export CROSSREF_EMAIL='your@email.com'

# Call your script with Automator's input
"/Users/YOURUSER/literature-review-scripts/bin/normalize-filename" "$@"
```

The Action for the bibligraphy script is similar. The bibliography script

- gets the references in BibTeX
- has JabRef make reasonable keys
- builds a LaTeX file that generates in-text APA citations for all of the references and then prints the bibliography.

The notion is that this would be a good enough start for some copy-paste way that you want to build a bibliography for a paper.
I always kept my references in bibtex, maintained mostly by hand in Emacs, and never understood why no one else I knew used a reference manager like EndNote or whatever, but maybe that's why I'm a computer consultant now and not an academic.

You can call the `pdftoapa` script with a list of PDFs or a single `bibtex.bib` file (the idea is that you could fix stuff that is wrong in JabRef and then print a clean bibliography).

# Stuff to Download arrticles from various publishers follows.

At some point I should split this stuff out to a separate REPO.

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

Will download all Wiley journals the list that Constellate generated
that includes one of the WORDS from all Wiley journals from 5ca9272b-bed8-f648-4089-264539d883a0-sampled-metadata.csv
which Constellate claims is all of the ones with one of the THREE WORDS in the journals it knows about.

First it gets DOIs from wiley-dois.txt (john wiley... from constellate)

Seconds it gets DOIS from wiley2-tesol-quarterly.txt (just wiley constellate)

Also gets DOIS from tq-all-dois.txt. That file was generated from TQ_All3.txt that were downloaded from somewhere into a Endnote file that was exported to "all fields" (has lines like FIELDNAME: XXX, DOI: xxx).
