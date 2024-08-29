#!/usr/bin/env python3
# Looks for DOI in XML input generatedy by doi.crossref.org and prints it to stdout
import xml.etree.ElementTree as ET
import sys

# Read XML input from stdin
xml_string = sys.stdin.read()

# Parse the XML
tree = ET.ElementTree(ET.fromstring(xml_string))
root = tree.getroot()

# Namespace dictionary to handle namespaces in the XML
namespaces = {'ns': 'http://www.crossref.org/qrschema/2.0'}

# Find the <doi> element and retrieve its text content
doi_element = root.find('.//ns:doi', namespaces)
doi_text = doi_element.text if doi_element is not None else None

print(doi_text)
