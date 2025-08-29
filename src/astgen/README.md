# src/astgen

AST generation for OPLang using the ANTLR visitor.

## Purpose
- Converts ANTLR parse trees into AST nodes defined in `src/utils/nodes.py`.
- Provides a single entry point `ASTGeneration` that walks the parse tree and builds the AST.

## Key files
- `ast_generation.py`: `ASTGeneration` class that extends `OPLangVisitor` and implements visit methods for:
  - Class/method/attribute/constructor/destructor declarations
  - Types (primitive, array, class, reference)
  - Expressions (binary, unary, postfix access, method calls, object creation)
  - Statements (block, assignment, if, for, break, continue, return)

## Notes
- The visitor returns strongly typed AST nodes (e.g., `ClassDecl`, `MethodDecl`, `BinaryOp`).
- Postfix expressions are built by accumulating postfix operators (member access, calls, array access).
