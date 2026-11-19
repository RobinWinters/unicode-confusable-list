#!/usr/bin/env python3
"""List lookalikes from a pinned subset, not the full Unicode confusables database."""
import argparse
import csv
from pathlib import Path
import sys

# Frozen local table subset-1. No downloaded or runtime Unicode confusable data.
# Key: ASCII comparison character; members: visually similar non-ASCII characters.
GROUPS = {
    'A': '\u0391\u0410', 'B': '\u0392\u0412', 'C': '\u0421',
    'E': '\u0395\u0415', 'H': '\u0397\u041d', 'I': '\u0399\u0406',
    'K': '\u039a\u041a', 'M': '\u039c\u041c', 'O': '\u039f\u041e',
    'P': '\u03a1\u0420', 'T': '\u03a4\u0422', 'X': '\u03a7\u0425',
    'Y': '\u03a5\u04ae', 'a': '\u0430', 'c': '\u0441', 'e': '\u0435',
    'i': '\u0456', 'j': '\u0458', 'o': '\u03bf\u043e',
    'p': '\u03c1\u0440', 's': '\u017f', 'x': '\u0445', 'y': '\u0443',
}
LOOKUP = {char: target for target, members in GROUPS.items() for char in members}
FIELDS = ['line', 'column', 'offset', 'character', 'codepoint', 'ascii_target', 'group_codepoints']


def scan(text):
    """One-based LF lines/codepoint columns; zero-based codepoint offset."""
    findings = []
    line, column = 1, 1
    for offset, char in enumerate(text):
        if char in LOOKUP:
            target = LOOKUP[char]
            group = target + GROUPS[target]
            findings.append(dict(line=line, column=column, offset=offset, character=char,
                                 codepoint='U+%04X' % ord(char), ascii_target=target,
                                 group_codepoints=' '.join('U+%04X' % ord(c) for c in group)))
        if char == '\n':
            line, column = line + 1, 1
        else:
            column += 1
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='UTF-8 text; optional initial BOM is removed')
    args = parser.parse_args(argv)
    try:
        findings = scan(Path(args.input).read_bytes().decode('utf-8-sig'))
    except (OSError, UnicodeError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 1
    writer = csv.DictWriter(sys.stdout, FIELDS, lineterminator='\n')
    writer.writeheader()
    writer.writerows(findings)
    return 0


if __name__ == '__main__':
    sys.exit(main())
