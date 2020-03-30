#!/usr/bin/python3

import html
import re
import sys

import os
import time

from datetime import date

headingMatcher = re.compile(r'^(#{1,6})(.*)')
linkMatcher = re.compile(r'\[(.+)\]\(([^\)]*)\)')
# inline code regex
codeMatcher = re.compile('`([^`]+)`')
boldMatcher = re.compile('__(.+?)__')
italicMatcher = re.compile('_(.+?)_')

bigSquare = """\
<svg width="3em" height="3em" style="float:left; vertical-align:middle;padding-right: 1em">
<a href="index.html"><rect x="0" y="0" width="3em" height="3em" rx="0.5em" ry="0.5em"/></a>
</svg>
"""

title = None
codeMode = False
paragraphMode = False
listMode = False

def codeEscape(match):
    """Returns the HTML from a regex match of inline code"""
    return f'<code>{html.escape(match.group(1))}</code>'

def processInline(line):
    """Creates HTML for a single line of markdown"""
    if codeMode:
        return html.escape(line)

    # INLINE CODE
    # inline code must be first because it html escapes its contents
    line = codeMatcher.sub(codeEscape, line)

    # LINKS
    line = linkMatcher.sub(r'<a href="\2">\1</a>', line)

    # BOLD
    line = boldMatcher.sub(r'<b>\1</b>', line)
    # ITALIC
    line = italicMatcher.sub(r'<i>\1</i>', line)

    return line

def processLine(line):
    """Processes the structure of a markdown file one line at a time"""
    global paragraphMode
    global title
    global codeMode
    global listMode

    # HORIZONTAL RULE
    if line == '---\n':
        return '<hr>'

    # HEADINGS
    headm = headingMatcher.match(line)
    if headm:
        paragraphMode = False
        poundCount = len(headm.group(1))
        content = headm.group(2).strip();

        idval = content
        idval.replace(' ', '_')

        if not title and poundCount == 1:
            title = content;
            return bigSquare + f'<h1 class="title" id="{idval}">{content}</h1>'
        return f'<h{poundCount} id="{idval}">{content}</h{poundCount}>'

    # CODE BLOCK
    if line[:3] == '```':
        paragraphMode = False
        res = '</code>' if codeMode else '<code class="codeBlock">' 
        codeMode = not codeMode
        return res

    # UNORDERED LIST
    if line[:2] == '- ':
        res = '<ul><li>' if not listMode else '</li><li>'
        listMode = True
        return res + processInline(line[2:])
    elif listMode and line == '\n':
        listMode = False
        return '</li></ul>' + processLine(line)
    elif listMode:
        return processInline(line)

    # PARAGRAPH
    if not paragraphMode and not codeMode and line != '\n':
        paragraphMode = True
        return '<p>\n' + processInline(line)
    elif paragraphMode and line == '\n':
        paragraphMode = False
        return '</p>\n'
    return processInline(line)

# input files: source.md, template.html
# output: source.html

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <file.md>')

    sourceName = sys.argv[1]
    baseName = sourceName.split('.')[0]
    targetName = baseName + '.html'

    with open(sourceName, 'r') as source, \
         open('template.html', 'r') as template, \
         open(targetName, 'w') as target:

        pageBody = [processLine(line) for line in source]
        for tline in template:
            if tline == '<!-- title -->\n':
                target.write(f'<title>{title}</title>\n')
            elif tline == '<!-- body -->\n':
                target.write(tline)
                for pline in pageBody:
                    target.write(pline)
            elif tline == '<!-- footer -->\n':
                mtime = os.stat(sourceName).st_mtime
                lastChange = time.strftime('%Y-%m-%d', time.localtime(mtime))
                target.write(f'<p>Last updated on {lastChange}</p>')
            else:
                target.write(tline)
