'''
The goal of this program is to take a set of cross-linked markdown files 
and generate from them one flat markdown file prior to passing it to a 
program like pandoc or mmd.

USAGE: 
	$ python mergedmd.py
	$ pandoc -s --to="html" lexicon-$(date +%Y-%m-%d).md > lexicon-$(date +%Y-%m-%d).html
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

with open("lexicon-"+datetime.datetime.utcnow().date().isoformat()+".md","w") as out:
	for f in allfiles:
		print >> out, '\n\n<a name="'+f[3:]+'"></a>\n'
		with open(f) as fp:
			s = fp.read().strip()
			s = mdlink2.sub(r'](\1)', s)
			s = mdlink.sub(r'](#\1)', s)
			s = mdhreflink.sub(r'href="\1"', s)
			s = mdhreflink2.sub(r'href="#\1"', s)
			print >> out, s
