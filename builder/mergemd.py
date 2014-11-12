'''
The goal of this program is to take a set of cross-linked markdown files 
and generate from them one flat markdown file prior to passing it to a 
program like pandoc or mmd.

The cover text is intended for posting on fhiso.org/lexeg/somepage.

USAGE: 
	$ python mergedmd.py
	$ pandoc --to="html" lexicon-$(date +%Y-%m-%d).md > lexicon-$(date +%Y-%m-%d).html
'''

import re, glob, datetime

anchors = {}

mdhreflink = re.compile(r'href="[^"]*\.md(#[^"]+)"')
mdhreflink2 = re.compile(r'href="([^"#]*\.md)"')
mdlink = re.compile(r'(?<!\\)\]\s*\(([^\)/]*)\)')
mdlink2 = re.compile(r'\]\s*\([^\)/]+md#([^\)/#]*)\)')

allfiles = glob.glob("../*.md")
allfiles.sort(lambda a,b: cmp(a.lower(), b.lower()))
allfiles.remove("../README.md")
allfiles.remove("../SOURCES.md")
allfiles.append("../SOURCES.md")
today = datetime.datetime.utcnow().date().isoformat()

def processMD(out, f, quoteLevel=0):
	print >> out, '\n\n<a name="'+f[3:]+'"></a>\n'
	with open(f) as fp:
		s = fp.read().strip()
		s = mdlink2.sub(r'](\1)', s)
		s = mdlink.sub(r'](#\1)', s)
		s = mdhreflink.sub(r'href="\1"', s)
		s = mdhreflink2.sub(r'href="#\1"', s)
		print >> out, ">"*quoteLevel + s.replace("\n","\n"+">"*quoteLevel)



with open("lexicon-"+today+".md","w") as out:
	print >> out, "#Lexicon snapshot ("+today+")#"
	print >> out, ""
	print >> out, """This lexicon is an auto-generated snapshot of the individual markdown files contained in the main directory of the lexicon exploratory group's github repository.  See <a href="..">the lexicon exploratory group's main page</a> for more."""
	print >> out, ""
	
	print >> out, "The README for this project contains the following:"
	print >> out, ""
	processMD(out, "../README.md", quoteLevel=1);
	
	print >> out, "\n\n"
	print >> out, "Lexicon Entries"
	print >> out, "==============="
	
	for f in allfiles:
		processMD(out, f)
