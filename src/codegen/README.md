# src/codegen

JVM bytecode generation for OPLang using Jasmin.

## Purpose
- Traverses the AST and emits Jasmin assembly (.j) files in `src/runtime/`.
- Handles class generation, fields, methods, constructors, destructors, and static initialization.

## Key files
- `codegen.py`: `CodeGenerator` visitor that drives code emission and manages per-class output.
- `emitter.py`: `Emitter` helper with JVM instruction helpers and stack bookkeeping.
- `frame.py`: `Frame` class for scope labels, operand stack tracking, and local variable indices.
- `utils.py`: Codegen symbols (`Symbol`, `Index`, `Access`, `SubBody`) and helper types.
- `io.py`: Built-in I/O symbol table used during code generation.
- `jasmin_code.py`: Low-level instruction templates used by `Emitter`.
- `error.py`: Runtime/codegen exceptions.

## Behavior highlights
- Emits class prolog/epilog, fields, and default constructors when none are defined.
- Generates `<clinit>` for static field initialization.
- Supports a `dispose` method to model destructors.
- Injects a Java-compatible `main` method when needed.

## Notes
- Code generation relies on `Emitter` for JVM type descriptors and stack discipline.
- Some visitor methods are still under active development; check TODOs in `codegen.py` if extending support.
