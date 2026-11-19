# Expected fixtures

- `clean.txt`: CSV header only; ASCII comparison characters are not findings on their own.
- `cyrillic.txt`: four findings at columns 2, 5, 8, and 11 on line 1; targets A, a, C, and c.
- `greek.txt`: four findings at columns 2, 5, 8, and 11 on line 1; targets O, o, P, and p.
- `mixed.txt`: Cyrillic and Greek uppercase A lookalikes at line 1 columns 2 and 3 share one group; Latin long s at line 2 column 6 targets ASCII s.

Locations count Unicode codepoints, not encoded bytes or display cells. The table is a pinned subset, not the full Unicode confusables database.
