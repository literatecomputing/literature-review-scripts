#!/usr/bin/env python3

# Try to clean up the consellate data and find real DOIs for bogus jstor ones
# reads a consellate.xlsx file and writes a consellate_updated.xlsx file that adds some columns.
# We ended up not using constellate for this project, but this script was useful for finding the real DOIs for some of the bogus jstor ones.
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os
from openpyxl import load_workbook
import subprocess
from urllib.parse import urlparse, urlunparse



current_directory = os.getcwd()
# get user email from the environment $CROSSREF_EMAIL
USER = os.environ.get('CROSSREF_EMAIL')
# Exit if the user email is not set
if USER is None:
    print("Please set the CROSSREF_EMAIL environment variable", file=sys.stderr)
    sys.exit(1) 

PROXY_SUFFIX = os.environ.get('PROXY_SUFFIX')
if PROXY_SUFFIX is None:
    print("Please set the PROXY_SUFFIX environment variable", file=sys.stderr)
    sys.exit(1)

def use_vu_proxy(url):
    # assumes that your library proxy works by changing the hostname dots to dashes and appending a suffix
    # Parse the URL into components
    parsed_url = urlparse(url)
    # Replace dots with dashes in the hostname
    modified_hostname = parsed_url.hostname.replace('.', '-')
    # Append the suffix to the modified hostname
    new_hostname = f"{modified_hostname}.{PROXY_SUFFIX}"
    # Reconstruct the URL with the new hostname
    modified_url = urlunparse(parsed_url._replace(netloc=new_hostname))
    return modified_url

def check_redirect(url):
    # Define the curl command with the necessary options
    curl_command = [
        'curl',
        '-s',      # Silent mode
        '-L',      # Follow redirects
        '-I',      # Fetch the headers only
        '-o', '/dev/null',  # Discard output
        '-w', '%{url_effective}',  # Output the final URL after all redirects
        url
    ]

    try:
        # Execute the curl command and capture the output
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        final_url = result.stdout.strip()
        return final_url

    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        return None


# Load the Excel file
df = pd.read_excel("consellate.xlsx")
df.insert(df.columns.get_loc('doi') + 1, 'download_filename', '')
df.insert(df.columns.get_loc('doi') + 1, 'download_url', '')
df.insert(df.columns.get_loc('doi') + 1, 'doi_match', '')
df.insert(df.columns.get_loc('doi') + 1, 'crossref_doi', '')
df = df.fillna('')

# Iterate over each row
for index, row in df.iterrows():
    # Get the hyperlink from the "doi" column plus .pdf
    hyperlink = str(row["doi"]) + ".pdf"

    # Extract the file path from the hyperlink (assuming it's in the same directory)
    file_path = os.path.join(current_directory, hyperlink)

    # Check if the file exists
    file_exists = os.path.exists(file_path)

    # print(f"{file_path} exists? #{file_exists}")

    # Update the "File-exists" column
    df.at[index, "File-exists"] = file_exists


    # User details
    doi = str(row['doi'])
    JNL = str(row['isPartOf'])
    VOL = str(row['volumeNumber'])
    ISSUE = str(row['issueNumber']).replace("Supplement ","S")
    PAGE = str(row['pageStart'])
    YEAR = str(row['publicationYear']) # screw the year

    # Encode the journal title to URL format
    JNL_encoded = requests.utils.quote(JNL)

    # Construct the URL
    url = f"https://doi.crossref.org/openurl?pid={USER}&title={JNL_encoded}&volume={VOL}&issue={ISSUE}&spage={PAGE}&redirect=false"


    if (doi == ""):
        final_url = None
    else:
         # See if it's a jstor URL
        final_url = check_redirect(f"https://doi.org/{doi}")

    if (final_url is not None) and ("cambridge.org" in final_url):
        download_filename = final_url.split("/")[-1]
        download_url = final_url.replace("www.cambridge.org",f"www-cambridge.org.{PROXY_SUFFIX}")
        df.at[index, "download_filename"] = download_filename
        df.at[index, "download_url"] = download_url

    if (final_url is not None) and ("sagepub.com" in final_url):
        # https://journals.sagepub.com/doi/10.1177/13670069211016546

        download_filename = final_url.split("/")[-1]
        download_url = final_url.replace("journals.sagepub.com",f"journals-sagepub-com.{PROXY_SUFFIX}").replace("/doi/","/doi/pdf/") + "?download=true"
        df.at[index, "download_filename"] = download_filename
        df.at[index, "download_url"] = download_url

    if (final_url is not None) and ("muse.jhu.edu" in final_url):
        download_filename = final_url.split("/")[-1]
        download_url = final_url.replace("muse.jhu.edu",f"muse-jhu-edu.{PROXY_SUFFIX}")
        df.at[index, "download_filename"] = download_filename
        df.at[index, "download_url"] = download_url

    # if it's not broken and not jstor bogus, skip
    if (final_url is not None) and ("doi.org" not in final_url) and ("jstor.org" not in final_url) :
        print (f"Real url: {final_url}")
        continue

    # Perform the HTTP GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Read the XML content from the response
        xml_string = response.text

        # Parse the XML
        tree = ET.ElementTree(ET.fromstring(xml_string))
        root = tree.getroot()

        # Namespace dictionary to handle namespaces in the XML
        namespaces = {'ns': 'http://www.crossref.org/qrschema/2.0'}

        # Find the <doi> element and retrieve its text content
        doi_element = root.find('.//ns:doi', namespaces)
        doi_text = doi_element.text if doi_element is not None else None
        # Update the "crossref_doi" column
        print(f"---> {doi}: Looking at {url}. Got {doi_text}--Match? #{doi_text==doi}")
        #time.sleep(2)
        df.at[index, "crossref_doi"] = doi_text
        df.at[index, "doi_match"] = doi_text==doi
        if ("10.1353" in doi_text):
            print "JHU"
            download_filename = final_url.split("/")[-1]
            download_url = final_url.replace("muse.jhu.edu",f"muse-jhu-edu.{PROXY_SUFFIX}")
            df.at[index, "download_filename"] = download_filename
            df.at[index, "download_url"] = download_url
        if ("10.1558" in doi_text):
            # https://journal.equinoxpub.com/Calico/article/view/16301
            # doesn't look like a way to get to the PDF
            final_url = check_redirect(f"https://doi.org/{doi_text}")
            download_filename = final_url.split("/")[-1]
            download_url = use_vu_proxy(final_url)
            df.at[index, "download_filename"] = download_filename
            df.at[index, "download_url"] = download_url

        if ("10.2307" in doi_text):
            # jstor
            final_url = check_redirect(f"https://doi.org/{doi_text}")
            download_filename = final_url.split("/")[-1]
            download_url = use_vu_proxy(final_url)
            df.at[index, "download_filename"] = download_filename
            df.at[index, "download_url"] = download_url

        if ("10.1017" in doi_text):
            download_filename = final_url.split("/")[-1]
            download_url = final_url.replace("www.cambridge.org",f"www-cambridge.org.{PROXY_SUFFIX}")
            df.at[index, "download_filename"] = download_filename
            df.at[index, "download_url"] = download_url
        if ("10.1177" in doi_text) or ("10.1191" in doi_text):
            download_filename = final_url.split("/")[-1]
            download_url = final_url.replace("journals.sagepub.com",f"journals-sagepub-com.{PROXY_SUFFIX}").replace("/doi/","/doi/pdf/") + "?download=true"
            df.at[index, "download_filename"] = download_filename
            df.at[index, "download_url"] = download_url

        print( f"{doi_text}=={doi} ? {doi_text==doi}")

    else:
        print(f"Failed to retrieve data: {response.status_code}", file=sys.stderr)

# Save the updated DataFrame to a new Excel file
df.to_excel("consellate_updated.xlsx", index=False)
