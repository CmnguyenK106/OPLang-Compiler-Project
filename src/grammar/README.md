# src/grammar

ANTLR4 grammar and lexer rules for OPLang.

## Purpose
- Defines the full language grammar in `OPLang.g4`, including declarations, statements, and expression precedence.
- Implements lexer error reporting for invalid characters, illegal escapes, and unclosed strings.

## Key files
- `OPLang.g4`: Parser and lexer rules for OPLang. Entry rule is `program` (one or more classes).
- `lexererr.py`: Exception classes used by the lexer (`ErrorToken`, `UncloseString`, `IllegalEscape`).

## Notes
- Lexer error handling is implemented in the `@lexer::members` section of `OPLang.g4`.
- Comments (`/* */` and `# ...`) and whitespace are skipped by the lexer.
