# Split the line
- Extract the title (`A`)
- Find the nearest tokens to `A` in the line
- Obtain their position and ignore *examples* and *alternative forms*

# Recognize examples
Args: *position* (of token in the line)
- `true` if the token contains `’` or `°`
