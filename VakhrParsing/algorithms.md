# Character classes
- Capital mansi character class (CMCC): `[А-ЯӒЁӇӦӰӘӚ]`
- Small mansi character class (SMCC): `[а-яӓёӈӧӱәӛ]`
- SMCC & PUNCT: `[а-яӓёӈӧӱәӛ\,\-\s]`

# Ignore lines
- `YES` if line ~ `^ \s* \d+ \s* $`
- Function *regex_for_lines(LINE_NUMBER, REGEXP)*
  - split REGEXP by `r'\n'` => Array, each element should be equal to a single line
  - first element is the current line (by default)
  - all next elements should be next lines therefore
  - return (`True`/ count of patterns between two newlines) if there is total regex array and line array one to one correspondence
  - else return `False`
- `YES` if:
  - *regex_for_lines(..., REGEXP)* is `true` for *REGEXP* = `\n[{0}\-\s]+\n[{0}\-\s]+\n\d+\n`
  - *regex_for_lines(..., REGEXP)* is `true` for *REGEXP* = `\n\d+\n[{0}\-\s]+\n[{0}\-\s]+\n`
  - *regex_for_lines(..., REGEXP)* is `true` for *REGEXP* = `\n[{0}\-\s]+\s+\d+\s+[{0}\-\s]+\n`
  - *regex_for_lines(..., REGEXP)* is `true` for *REGEXP* = `\n\d+\n`
  - *regex_for_lines(..., REGEXP)* is `true` for *REGEXP* = `\n[A-Z{$CMCC}{$SMCC}\-\s]\n`
- `NO`: else


# Split lines
- Extract the title (`A`)
- Find the nearest tokens to `A` in the line (alphabet sort and string similarity)
- Obtain their position and ignore *examples* and *alternative forms*
- Split the line in all relevant positions

# Pre-format the line
- `A/B` OR `A/ B` -> `A /B`
- `A / B` -> `A /B` if `A` is russian and `B` is **not** russian
- case of `сп л отйт ь`
- case of `(по матерйнской / лйнии)/ӓ°щойкә`

# Join lines
- `YES`: join line **B** and line **A** if line **A** ends with `-` (`\s*-\s*$`)
- `NO`: else


# Recognize alternative forms
Args: *position* **N** (of token in the line)
- `true` if the token contains `’` or `°`
- `true` if `/` was found on the start of the token with position **N** (token groups may be taken into account)
- `true` if `/` was found on the start of a token with position **N**-**x** and all tokens with positions between **N** and **N**-**x** have `,` on the end; if there are token groups (but not single tokens) between `,` length of token groups must be equal
- `false`: else

# Recognize examples
- Function *regex_range(REGEXP)* that returns two integers, indices of the first and the last token matched.
- Character classes (see above)
- Regex for example range: `{$CMCC} {$SMMC&PUNCT}+ \s* [\.!\?] ( \s* {$CMMC} {$SMMC&PUNCT}+ \s* [\.!\?]* \s* ) ?`
- `true` if token position **IN** the range
- `false`: else
