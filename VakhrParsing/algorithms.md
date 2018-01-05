# Split the line
- Extract the title (`A`)
- Find the nearest tokens to `A` in the line
- Obtain their position and ignore *examples* and *alternative forms*

# Pre-format the line
- `A/B` -> `A /B`
- case of `сп л отйт ь`

# Recognize alternative forms
Args: *position* **N** (of token in the line)
- `true` if the token contains `’` or `°`
- `true` if `/` was found on the start of the token with position **N** (collocations may be taken into account)
- `true` if `/` was found on the start of a token with position **N**-**x** and all tokens with positions between **N** and **N**-**x** have `,` on the end (collocations may be taken into account)
- `false`: else

# Recognize examples
