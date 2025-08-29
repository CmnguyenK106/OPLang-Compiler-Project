# src/semantics

Static semantic analysis for OPLang.

## Purpose
- Validates OPLang programs after AST generation.
- Enforces scope rules, type rules, member access rules, and entry point requirements.

## Key files
- `static_checker.py`: `StaticChecker` visitor that walks the AST and performs semantic checks. It builds symbol tables for classes, members, and local scopes and reports errors through exceptions.
- `static_error.py`: Exception types for all semantic errors (e.g., `Redeclared`, `UndeclaredClass`, `TypeMismatchInStatement`).

## Behavior highlights
- Seeds built-in `io` class methods for type checking.
- Validates the presence of a `static void main()` entry point with no parameters.
- Checks class inheritance and member resolution across parent classes.

## Notes
- The checker contains TODO markers for staged tasks; use them as a guide when completing remaining rules.
