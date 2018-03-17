"""
MD-Preview

Preview markdown files directly in terminal
"""

import sys
import re


"""
Colors are defined here with ASCII escape codes
"""
class color:
    TITLE1 = '\033[92m'
    TITLE2 = '\033[96m'
    TITLE3 = '\033[94m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    END = '\033[0m'


"""
Replace _italic_ and **bold**
"""
def repFont(s):
    patterns = {"italic" : "(\s_|^_)(?=\S)([\s\S]*?\S)_(?![_\S])",
                "bold" : "(\s\*\*|^\*\*)(?=\S)([\s\S]*?\S)\*\*(?![\*\*\S])"}

    pat = re.compile(patterns["italic"])
    res = pat.findall(s)
    if res:
        for r in res:
            rep = ' ' + color.ITALIC + r[1] + color.END 
            s = re.sub(pat, rep, s, count=1)

    pat = re.compile(patterns["bold"])
    res = pat.findall(s)
    if res:
        for r in res:
            rep = ' ' + color.BOLD + r[1] + color.END
            rep = checkInTable(s, rep)
            s = re.sub(pat, rep, s, count=1)
    return s


"""
Replace Title
"""
def repTitle(s):
    splt = s.split(" ")
    title_lvl = splt[0]
    title = " ".join(splt[1:]).rstrip("\n")

    if title_lvl == "#":
        out = color.TITLE1 + color.BOLD + title.title() + '\n' + "="*len(title) + color.END
    elif title_lvl == "##":
        out = color.TITLE2 + color.BOLD + title.title() + '\n' + "-"*len(title) + color.END
    elif title_lvl == "###":
        out = color.TITLE3 + color.BOLD + title.title() + color.END
    elif title_lvl == "####":
        out = color.BOLD + title.title() + color.END
    else:
        out = title.title()
    return out


"""
Replace md **-symbol with spaces if in table
"""
def checkInTable(s, rep):
    if s[0] == "|":
        return rep + '    '
    else:
        return rep


"""
Main Method
"""
if __name__ == '__main__':
    filename = sys.argv[1]
    lines = open(filename).readlines()
    print("\n")
    for l in lines:
        if l[0] == '#':
            print(repTitle(l))
            continue

        l = repFont(l)
        print(l.rstrip('\n'))
    print("\n")
