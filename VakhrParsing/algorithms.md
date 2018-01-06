# Character classes
- Capital mansi character class (CMCC): `[А-ЯӒЁӇӦӰӘӚ]`
- Small mansi character class (SMCC): `[а-яӓёӈӧӱәӛ]`
- SMCC & PUNCT: `[а-яӓёӈӧӱәӛ\,-\s]`

# Ignore lines
- `YES` if line ~ `^ \s* \d+ \s* $`
- `YES` if:
```python
page_pattern = r'\n[{0}\-\s]+\n[{0}\-\s]+\n\d+\n|\n\d+\n[{0}\-\s]+\n[{0}\-\s]+\n|'
page_pattern += r'\n[{0}\-\s]+\s+\d+\s+[{0}\-\s]+\n|\n\d+\n|\n[A-Z{$CMCC}{$SMCC}]\n'
```

# Split lines
- Extract the title (`A`)
- Find the nearest tokens to `A` in the line (alphabet sort and string similarity)
- Obtain their position and ignore *examples* and *alternative forms*
- Split the line in all relevant positions

# Pre-format the line
- `A/B` OR `A/ B` -> `A /B`
- case of `сп л отйт ь`

# Join lines
- `YES`: join line **B** and line **A** if line **A** ends with `-` (`\s*-\s*$`)
- `NO`: else


# Recognize alternative forms
Args: *position* **N** (of token in the line)
- `true` if the token contains `’` or `°`
- `true` if `/` was found on the start of the token with position **N** (collocations may be taken into account)
- `true` if `/` was found on the start of a token with position **N**-**x** and all tokens with positions between **N** and **N**-**x** have `,` on the end (collocations may be taken into account)
- `false`: else

# Recognize examples
- Function *regex_range(REGEXP)* that returns two integers, indices of the first and the last token matched.
- Character classes (see above)
- Regex for example range: `{$CMCC} {$SMMC&PUNCT}+ \s* [\.!\?] ( \s* {$CMMC} {$SMMC&PUNCT}+ \s* [\.!\?]* \s* ) ?`
- `true` if token position **IN** the range
- `false`: else
