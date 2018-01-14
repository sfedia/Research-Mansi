# Character classes [solved]
- Capital mansi character class (CMCC): `[А-ЯӒЁӇӦӰӘӚ]`
- Small mansi character class (SMCC): `[а-яӓёӈӧӱәӛ]`
- SMCC & PUNCT: `[а-яӓёӈӧӱәӛ\,\-\s]`
- SMCC & PUNCT EXT: `[а-яӓёӈӧөӱәӛ\,\-\s\(\)]`

# Split lines
- Extract the title (`A`)
- Find the nearest tokens to `A` in the line (alphabet sort and string similarity)
- Obtain their position and ignore *examples*, *alternative forms* and russian words
- Split the line in all relevant positions

# Pre-format the line
- `A/B` OR `A/ B` -> `A /B` [solved]
- `A / B` -> `A /B` if `A` is russian and `B` is **not** russian [solved]
- case of `сп л отйт ь`
- case of `(по матерйнской / лйнии)/ӓ°щойкә`

# Join lines [solved]
- `YES` (via **whitespace**, `\s{2,}` -> ' '): join line **B** and line **A** if line **A** ends with `-` (`\s*-\s*$`)
- `YES` (via **whitespace**, `\s{2,}` -> ' '): join line **B** and line **A** if line **B** starts with `\s*\d+[\.,]`
- `YES` (via **whitespace**, `\s{2,}` -> ' '): join line **B** and line **A** if line **A** ends with `,` (`\s*,\s*$`)
- `YES` (via **whitespace**, `\s{2,}` -> ' '): join line **B** and line **A** if line **A** ends with `/` (`\s*\/\s*$`)
- `YES` (via **whitespace**, `\s{2,}` -> ' '): join line **B** and line **A** if the first tokens of lines **A**, **B** and **C** are sorted as [ **A**[0] , **C**[0], **B**[0] ]
- `NO`: else


# Recognize alternative forms
Args: *position* **N** (of token in the line)
- `true` if the token contains `’` or `°`
- `true` if `/` was found on the start of the token with position **N** (token groups may be taken into account)
- `true` if `/` was found on the start of a token with position **N**-**x** and all tokens with positions between **N** and **N**-**x** have `,` on the end; if there are token groups (but not single tokens) between `,` number of tokens in all (or at least 2) groups must be equal
  - case of `/1. ӓкӓк-өвәмл’ ӓптӓх,	ӓкӓн-өвәм-тӓптӓх; 2. ӓкӓн-ща°хщәй-тӓх, ӓкӓн-щӓ кщәйтӓх`
- `false`: else

# Recognize examples
- Function *regex_range(REGEXP)* that returns two integers, indices of the first and the last token matched.
- Character classes (see above)
- Regex for example range (ignore ws): `{$CMCC} {$SMCC&PUNCT_EXT}+ \s* [\.!\?] ( \s* {$CMCC} {$SMCC&PUNCT_EXT}+ \s* [\.!\?]* \s* ) ?`
- `true` if token position **IN** the range
- `false`: else
