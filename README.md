# Unicode confusable list

Open-source documentation maintainers can use this free offline scanner to locate selected visually similar characters in text. Its CSV points to individual characters so a maintainer can review whether each spelling is intentional. It includes Latin, Cyrillic, and Greek lookalikes alongside ASCII comparison characters. This is a frozen F6 utility for catalog spec 288.

## Pinned scope

The source embeds the local `subset-1` table. It is a small pinned subset, not the full Unicode confusables database. Its explicit groups cover selected uppercase Latin-shaped Greek and Cyrillic letters, selected lowercase Cyrillic and Greek letters, and Latin long s. Each group names an ASCII comparison character. Only non-ASCII table members become findings; an ASCII comparison character on its own is clean. A finding does not require both spellings to occur in the same file.

Input is UTF-8 text, optionally beginning with a BOM. Invalid UTF-8 is rejected. Locations use one-based line and column numbers and zero-based character offsets. Lines advance on LF; columns and offsets count Unicode codepoints, not bytes, grapheme clusters, or terminal cells. A carriage return occupies a column. The initial BOM is removed before location counting. Text is never normalized or rewritten, and the input file is never mutated.

Non-goals include comprehensive Unicode coverage, font-specific similarity, spoofing verdicts, domain-name analysis, language detection, and automated spelling repair. Characters outside the embedded table are ignored even when they might look similar in a particular font. Review a reported group in its document context before changing anything.

## Usage and checks

From this folder, run:

```text
python3 unicode_confusable_list.py fixtures/mixed.txt
python3 -m unittest
```

CSV columns are `line,column,offset,character,codepoint,ascii_target,group_codepoints`. Findings follow source order; group membership is frozen in the source. A clean scan prints only the header. Exit code 0 means the scan succeeded, including when findings exist; nonzero means unreadable or invalid input or arguments. Errors go to standard error. The synthetic fixtures cover clean ASCII, Cyrillic, Greek, and mixed-script groups. Tests also exercise multibyte location counting and characters outside the subset. Only Python 3 and its standard library are required, with no network access.

Frozen release. No updates, no support, no roadmap are promised. Later distribution uses the held GitHub repository/profile and repository search; this folder publishes nothing.

## Support

Voluntary one-time support only via the held Stripe support rail, with utility attribution retained at publication.

Support link: https://buy.stripe.com/bJe28qgTC3es7VmepLa7C01

Counting path: voluntary support payment -> Stripe payment link -> Mercury, Plaid-verified; a support payment is counted once, shared rail across utilities is never double-counted. The held Stripe payout reaches Mercury through its partner bank. Producing this utility creates infrastructure; only an attributed support payment settled to Mercury counts as income.
