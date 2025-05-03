#!/usr/bin/env python
import getopt
import os
import subprocess
from lxml import etree, html
import chardet

dtype = "text/html"

clip_command = ["xclip", "-selection", "clipboard", "-o", "-t", dtype]
tidy_command = ["tidy", "-qi", "--wrap", "0"]

try:
    htmlclip = subprocess.check_output(clip_command + tidy_command)
except subprocess.CalledProcessError as e:
    exit(1)

if dtype == "text/html":
    # Parse the HTML
    try:
        parser = html.HTMLParser()
        tree = html.fromstring(htmlclip, parser=parser)
    except etree.XMLSyntaxError as e:
        print("Error parsing HTML:", e)
        exit(1)

    # Convert the HTML to a string
    htmlclip = etree.tostring(tree, encoding="utf-8", pretty_print=True)

encoding = chardet.detect(htmlclip)["encoding"]

# Shove the clipboard to a temporary file
tmpfn = "/tmp/htmlclip_%i" % os.getpid()

print("Writing to %s" % tmpfn)

with open(tmpfn, "w") as editfile:
    editfile.write(htmlclip.decode(encoding))

# Manually edit the temporary file
subprocess.call(["nvim", tmpfn])

print("Reading from %s" % tmpfn)

# call 'cat tmpfn | xclip -selection clipboard -t text/html'
subprocess.call(
    ["xclip", "-selection", "clipboard", "-t", dtype, tmpfn],
    stdin=open(tmpfn, "r"),
)





