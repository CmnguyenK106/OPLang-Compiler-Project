"""
Code Generator for OPLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from platform import node
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter, is_void_type, is_int_type, is_string_type, is_bool_type, is_float_type
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *

VoidType = PrimitiveType("void")
IntType = PrimitiveType("int")
FloatType = PrimitiveType("float")
BoolType = PrimitiveType("boolean")
StringType = PrimitiveType("string")

# Add this helper function
def check_type(node, type_name):
    """Safe check for PrimitiveType instances."""
    return isinstance(node, PrimitiveType) and node.type_name == type_name

class CodeGenerator(ASTVisitor):
    """
    Code generator for OPLang.
    Traverses AST and generates JVM bytecode.
    """
    
    def __init__(self):
        self.current_class = None
        self.parent_class = None
        self.program_name = None
        self.current_class_node = None
        self.main_injection = None
        self.emit = None  # Will be initialized per class
        self.rhs = None
        self.list_class: List[ClassDecl] = [
            ClassDecl("io", None, [
                MethodDecl(True, PrimitiveType("int"), "readInt", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeInt", [Parameter(PrimitiveType("int"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeIntLn", [Parameter(PrimitiveType("int"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("float"), "readFloat", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeFloat", [Parameter(PrimitiveType("float"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeFloatLn", [Parameter(PrimitiveType("float"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("boolean"), "readBool", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeBool", [Parameter(PrimitiveType("boolean"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeBoolLn", [Parameter(PrimitiveType("boolean"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("string"), "readStr", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeStr", [Parameter(PrimitiveType("string"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeStrLn", [Parameter(PrimitiveType("string"), "anArg")], BlockStatement([], [])),
            ])
        ]

    
    # ============================================================================
    # Program and Class Declarations
    # ============================================================================

    def visit_program(self, node: "Program", o: Any = None):
        """
        Visit program node - generate code for all classes.
        """
        try:
            # 1. Register classes first
            self.list_class += node.class_decls
            
            # 2. Set Program Name
            self.program_name = node.class_decls[0].name if node.class_decls else "Main"
            
            # 3. Main Injection (optional)
            self.main_injection = None 
            main_class_decl = None
            for class_decl in node.class_decls:
                for member in class_decl.members:
                    if hasattr(member, 'name') and member.name == "main":
                        main_class_decl = class_decl
                        self.main_injection = member
                        break
                if self.main_injection: 
                    break
            
            if main_class_decl and main_class_decl.name == self.program_name:
                self.main_injection = None

            # 4. Visit Classes
            for class_decl in node.class_decls:
                self.visit(class_decl, o)
                
        except Exception as e:
            # ĐOẠN NÀY SẼ IN LỖI THỰC SỰ RA MÀN HÌNH
            print("\n" + "="*30)
            print(f"!!! COMPILER CRASH !!!")
            print(f"Lỗi: {e}")
            import traceback
            traceback.print_exc()
            print("="*30 + "\n")
            raise e # Ném lỗi lại để Test Runner biết là fail

    def visit_class_decl(self, node: "ClassDecl", o: Any = None):
        """
        Visit Class Declaration.
        Flow:
        1. Prolog
        2. Generate Fields (Fix Unknown field error)
        3. Generate Default Constructor
        4. Generate Methods (includes Main Injection)
        5. Generate Static Initializer (Fix Static assignment error)
        6. Epilog
        """
        self.current_class = node.name
        self.current_class_node = node

        self.parent_name = node.superclass if node.superclass else "java/lang/Object"
        
        # 1. Setup Emitter
        filename = f"{node.name}.j"
        self.emit = Emitter(filename)
        parent = node.superclass if node.superclass else "java/lang/Object"
        self.emit.print_out(self.emit.emit_prolog(node.name, parent))
        
        # 2. Sinh Fields (Attributes)
        for member in node.members:
            if isinstance(member, AttributeDecl):
                self.visit(member, o)

        # ---------------------------------------------------------
        # 3. SINH METHODS VÀ CONSTRUCTORS
        # ---------------------------------------------------------
        has_init = False  # Cờ kiểm tra xem User có định nghĩa constructor không
        
        for member in node.members:
            # Case A: Constructor do User định nghĩa
            if isinstance(member, ConstructorDecl):
                has_init = True
                self.visit(member, o)
            
            # Case B: Method thông thường
            elif isinstance(member, MethodDecl):
                # [FIX QUAN TRỌNG]: Nếu đây là hàm main của chương trình chính,
                # TA PHẢI BỎ QUA (CONTINUE) ở đây.
                # Lý do: Nó sẽ được sinh bởi gen_main_method ở cuối hàm.
                # Nếu không skip, visit_method_decl sẽ sinh ra nó 1 lần, 
                # và gen_main_method sinh lại lần 2 -> Duplicate Method Error.
                if self.main_injection and member == self.main_injection and node.name == self.program_name:
                    continue
                
                self.visit(member, o)
            elif isinstance(member, DestructorDecl):
                self.visit(member, o)

        # ---------------------------------------------------------
        # 4. Kiểm tra sinh Default Constructor (Nếu user không viết)
        # ---------------------------------------------------------
        if not has_init:
            # Sinh: public <init>() { super(); }
            self.emit.print_out(self.emit.emit_method("<init>", FunctionType([], PrimitiveType("void")), False))
            
            frame = Frame("<init>", PrimitiveType("void"))
            frame.enter_scope(False)
            frame.get_new_index() # Index 0 cho 'this'
            
            self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
            self.emit.print_out(self.emit.emit_read_var("this", ClassType(node.name), 0, frame))
            self.emit.print_out(self.emit.emit_invoke_special(frame, f"{parent}/<init>", FunctionType([], PrimitiveType("void"))))
            
            self.emit.print_out(self.emit.emit_return(PrimitiveType("void"), frame))
            self.emit.print_out(self.emit.emit_end_method(frame))
            frame.exit_scope()

        # 5. Inject Main (Chỉ sinh 1 lần tại đây)
        if self.main_injection and node.name == self.program_name:
            self.gen_main_method(self.main_injection, o)

        # ---------------------------------------------------------
        # BƯỚC 4: SINH STATIC INITIALIZER (<clinit>)
        # ---------------------------------------------------------
        static_stmts = []
        for member in node.members:
            if isinstance(member, AttributeDecl):
                is_static = False
                if member.is_static: is_static = True
                    
                if is_static:
                    for attr in member.attributes:
                        if attr.init_value:
                            lhs = Identifier(attr.name)
                            lhs.type = member.attr_type 
                            assign = AssignmentStatement(lhs, attr.init_value)
                            static_stmts.append(assign)

        if static_stmts:
            self.emit.print_out(self.emit.emit_method("<clinit>", FunctionType([], VoidType), True))
            
            clinit_frame = Frame("<clinit>", VoidType)
            clinit_frame.enter_scope(True) 
            
            self.emit.print_out(self.emit.emit_label(clinit_frame.get_start_label(), clinit_frame))
            
            for stmt in static_stmts:
                # 1. RHS
                rhs_code, rhs_type = self.visit(stmt.rhs, Access(clinit_frame, [], False))
                self.emit.print_out(rhs_code)
                
                # 2. Coercion
                lhs_type = stmt.lhs.type
                def is_int(t): return isinstance(t, PrimitiveType) and t.type_name == "int"
                def is_float(t): return isinstance(t, PrimitiveType) and t.type_name == "float"

                if is_float(lhs_type) and is_int(rhs_type):
                     self.emit.print_out(self.emit.emit_i2f(clinit_frame))
                
                # 3. Putstatic (Dùng dấu / )
                field_ref = f"{self.current_class}/{stmt.lhs.name}"
                self.emit.print_out(self.emit.emit_put_static(field_ref, lhs_type, clinit_frame))
            
            self.emit.print_out(self.emit.emit_return(VoidType, clinit_frame))
            self.emit.print_out(self.emit.emit_end_method(clinit_frame))
            clinit_frame.exit_scope()

        # --- EPILOG ---
        self.emit.emit_epilog()

    def gen_main_method(self, node, o):
        """
        Helper to generate the public static void main explicitly.
        """
        # 1. Define Standard Java Main Signature
        # Use StringType directly (no brackets)
        method_type = FunctionType([ArrayType(StringType, 0)], VoidType)
        
        # Create a fresh frame
        frame = Frame("main", VoidType)
        frame.enter_scope(True)
        
        # --- [FIX BUG TẠI ĐÂY] ---
        # Hàm main chuẩn của Java luôn có tham số String[] args tại index 0.
        # Ta cần cấp phát index này để .limit locals ít nhất là 1.
        frame.get_new_index() 
        # -------------------------
        
        # 2. Emit Method Header
        self.emit.print_out(self.emit.emit_method("main", method_type, True))
        
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
        
        # 3. Visit Body
        # We use empty symbol list for main
        self.visit(node.body, Access(frame, [], False))
        
        # 4. Emit Return and End
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        self.emit.print_out(self.emit.emit_return(VoidType, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()

    # ============================================================================
    # Attribute Declarations
    # ============================================================================

    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None):
        """
        Visit attribute declaration - generate field directives.
        TODO: Implement attribute initialization if needed
        """
        for attr in node.attributes:
            self.visit(attr, (node, o))

    def visit_attribute(self, node: "Attribute", o: Any = None):
        """
        Visit attribute.
        Handles both Definition (Class Declaration) and Initialization (Constructor/Static Block).
        """
        # Unpack the context passed from visit_attribute_decl
        # attr_decl: The parent AttributeDecl (contains type, static/final flags)
        # context: None (Definition Mode) OR Frame (Initialization Mode)
        attr_decl, context = o
        
        # ---------------------------------------------------------
        # MODE 1: DEFINITION (Generating .field directives)
        # ---------------------------------------------------------
        if context is None:
            if attr_decl.is_static:
                # Static Field
                # value=None because initial value is handled in <clinit>
                self.emit.print_out(self.emit.emit_attribute(
                    node.name,
                    attr_decl.attr_type,
                    attr_decl.is_final,
                    None 
                ))
            else:
                # Instance Field
                self.emit.print_out(self.emit.jvm.emitINSTANCEFIELD(
                    node.name,
                    self.emit.get_jvm_type(attr_decl.attr_type)
                ))
            return

        # ---------------------------------------------------------
        # MODE 2: INITIALIZATION (Generating assignment code)
        # ---------------------------------------------------------
        frame = context
        
        # We only generate code if there is an initialization value (e.g., int a = 5;)
        if node.init_value:
            
            # --- CRITICAL FIX: Create a valid Access Context ---
            # We must construct a symbol table so visitors don't crash.
            sym = []
            if not attr_decl.is_static:
                 # If instance field, we have access to 'this' at index 0
                 sym = [Symbol("this", ClassType(self.current_class), Index(0))]
            
            # Wrap frame and sym into an Access object
            access = Access(frame, sym, False)
            # ---------------------------------------------------

            # A. STATIC INITIALIZATION (inside <clinit>)
            if attr_decl.is_static and frame.name == "<clinit>":
                # Generate Code for the Expression using 'access'
                code, type_ = self.visit(node.init_value, access)
                self.emit.print_out(code)
                
                # Coercion (Int -> Float)
                if check_type(attr_decl.attr_type, "float") and check_type(type_, "int"):
                    self.emit.print_out(self.emit.emit_i2f(frame))
                    
                # Store Value (putstatic)
                self.emit.print_out(self.emit.emit_put_static(
                    self.current_class + "/" + node.name,
                    attr_decl.attr_type,
                    frame
                ))

            # B. INSTANCE INITIALIZATION (inside <init>)
            elif not attr_decl.is_static and frame.name == "<init>":
                # 1. Load 'this' (Destination)
                self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
                
                # 2. Generate Code for the Expression
                code, type_ = self.visit(node.init_value, access)
                self.emit.print_out(code)
                
                # 3. Coercion
                if check_type(attr_decl.attr_type, "float") and check_type(type_, "int"):
                    self.emit.print_out(self.emit.emit_i2f(frame))
                    
                # 4. Store Value (putfield)
                self.emit.print_out(self.emit.emit_put_field(
                    self.current_class + "." + node.name,
                    attr_decl.attr_type,
                    frame
                ))
    

    # ============================================================================
    # Method Declarations
    # ============================================================================

    def visit_method_decl(self, node: "MethodDecl", o: Any = None):
        """
        Visit method declaration - generate method code.
        """
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, frame, node.is_static)

    # def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
    #     """
    #     Visit constructor declaration - generate constructor code.
    #     """
    #     # TODO 1: Implement constructor generation
    #     # 1. Setup Method Signature & Frame
    #     method_type = FunctionType([x.param_type for x in node.params], VoidType)
    #     frame = Frame("<init>", VoidType)
        
    #     self.emit.print_out(self.emit.emit_method("<init>", method_type, False))
        
    #     frame.enter_scope(False)
    #     self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))

    #     # 2. Reserve index 0 for 'this'
    #     frame.get_new_index() 
    #     this_sym = Symbol("this", ClassType(self.current_class), Index(0))
    #     env = [this_sym]
    #     body_access = Access(frame, env, False, True)

    #     # 3. Invoke Super Constructor
    #     self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
    #     self.emit.print_out(self.emit.emit_invoke_special(
    #         frame, 
    #         f"{self.parent_name}/<init>", 
    #         FunctionType([], VoidType)
    #     ))

    #     # =======================================================================
    #     # GENERATE INSTANCE FIELD INITIALIZATION
    #     # =======================================================================
    #     if self.current_class_node:
    #         for member in self.current_class_node.members:
    #             if isinstance(member, AttributeDecl):
    #                 # Check Static
    #                 is_static = False
    #                 if hasattr(member, 'kind') and str(member.kind) == 'Static': is_static = True
    #                 elif hasattr(member, 'is_static') and member.is_static: is_static = True
                    
    #                 if not is_static:
    #                     for attr in member.attributes:
    #                         if attr.init_value:
    #                             # A. Load 'this'
    #                             self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
                                
    #                             # B. Generate Init Value Code
    #                             init_code, init_type = self.visit(attr.init_value, body_access)
    #                             self.emit.print_out(init_code) 
                                
    #                             # C. Coercion (Int -> Float) [FIXED CHECK]
    #                             is_lhs_float = isinstance(member.attr_type, PrimitiveType) and member.attr_type.type_name == "float"
    #                             is_rhs_int = isinstance(init_type, PrimitiveType) and init_type.type_name == "int"

    #                             if is_lhs_float and is_rhs_int:
    #                                 self.emit.print_out(self.emit.emit_i2f(frame))
                                
    #                             # D. Putfield
    #                             self.emit.print_out(self.emit.emit_put_field(
    #                                 f"{self.current_class}/{attr.name}",
    #                                 member.attr_type,
    #                                 frame
    #                             ))
    #     # =======================================================================

    #     # 4. Visit Params 
    #     for param in node.params:
    #         idx = frame.get_new_index()
    #         # Handle param name attribute difference
    #         p_name = param.name
    #         p_type = param.param_type 
    #         param_sym = Symbol(p_name, p_type, Index(idx))
    #         env.insert(0, param_sym) 

    #     # 5. Visit Body
    #     self.visit(node.body, body_access)

    #     # 6. End Method
    #     self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
    #     self.emit.print_out(self.emit.emit_return(VoidType, frame))
    #     self.emit.print_out(self.emit.emit_end_method(frame))
        
    #     frame.exit_scope()

    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
        # 1. Setup Method Signature & Frame
        method_type = FunctionType([x.param_type for x in node.params], VoidType)
        frame = Frame("<init>", VoidType)
        
        self.emit.print_out(self.emit.emit_method("<init>", method_type, False))
        
        frame.enter_scope(False)
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))

        # 2. Reserve index 0 for 'this' & Setup Symbol Table
        frame.get_new_index() 
        this_sym = Symbol("this", ClassType(self.current_class), Index(0))
        env = [this_sym]
        body_access = Access(frame, env, False, True)

        # ---------------------------------------------------------
        # LOGIC GỌI SUPER CONSTRUCTOR
        # ---------------------------------------------------------
        # A. Load 'this' (emit_read_var TỰ ĐỘNG push stack)
        self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
        
        # B. Tìm Class Cha và Constructor khớp signature (Dùng Descriptor Check)
        parent_constructor_params = [] 
        match_found = False
        
        current_param_descs = [self.emit.get_jvm_type(p.param_type) for p in node.params]
        
        parent_node = None
        for c in self.list_class:
            if c.name == self.parent_name:
                parent_node = c
                break
        
        if parent_node:
            for m in parent_node.members:
                if isinstance(m, ConstructorDecl):
                    parent_param_descs = [self.emit.get_jvm_type(p.param_type) for p in m.params]
                    if current_param_descs == parent_param_descs:
                        parent_constructor_params = [p.param_type for p in m.params]
                        match_found = True
                        break

        # C. Sinh mã load tham số truyền lên Super
        if match_found:
             for i, param in enumerate(node.params):
                p_type = param.param_type
                idx = i + 1 
                
                type_desc = self.emit.get_jvm_type(p_type)
                
                # Sinh mã bytecode
                if type_desc == "I" or type_desc == "Z" or type_desc == "B" or type_desc == "S":
                    self.emit.print_out(self.emit.jvm.emitILOAD(idx))
                elif type_desc == "F":
                    self.emit.print_out(self.emit.jvm.emitFLOAD(idx))
                else:
                    self.emit.print_out(self.emit.jvm.emitALOAD(idx))
                
                # [FIX BUG QUAN TRỌNG]: Cập nhật Stack ảo!
                # Vì ta gọi jvm.emit... trực tiếp nên phải tự push thủ công.
                frame.push() 
        
        # D. Invoke Special (Lúc này stack ảo đã đủ: [this, arg1, arg2...])
        self.emit.print_out(self.emit.emit_invoke_special(
            frame, 
            f"{self.parent_name}/<init>", 
            FunctionType(parent_constructor_params, VoidType)
        ))

        # =======================================================================
        # GENERATE INSTANCE FIELD INITIALIZATION (Giữ nguyên)
        # =======================================================================
        if self.current_class_node:
            for member in self.current_class_node.members:
                if isinstance(member, AttributeDecl):
                    is_static = False
                    if hasattr(member, 'kind') and str(member.kind) == 'Static': is_static = True
                    elif hasattr(member, 'is_static') and member.is_static: is_static = True
                    
                    if not is_static:
                        for attr in member.attributes:
                            if attr.init_value:
                                self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
                                
                                init_code, init_type = self.visit(attr.init_value, body_access)
                                self.emit.print_out(init_code) 
                                
                                lhs_desc = self.emit.get_jvm_type(member.attr_type)
                                rhs_desc = self.emit.get_jvm_type(init_type)
                                
                                if lhs_desc == "F" and rhs_desc == "I":
                                    self.emit.print_out(self.emit.emit_i2f(frame))
                                
                                self.emit.print_out(self.emit.emit_put_field(
                                    f"{self.current_class}/{attr.name}",
                                    member.attr_type,
                                    frame
                                ))
        # =======================================================================

        # 4. Visit Params (Manual Handling)
        for param in node.params:
            idx = frame.get_new_index()
            p_name = param.name
            p_type = param.param_type 
            param_sym = Symbol(p_name, p_type, Index(idx))
            env.insert(0, param_sym) 

        # 5. Visit Body
        self.visit(node.body, body_access)

        # 6. End Method
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        self.emit.print_out(self.emit.emit_return(VoidType, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None):
        """
        Visit destructor declaration - generate destructor code.
        """
        method_name = "dispose"
        return_type = VoidType
        
        frame = Frame(method_name, return_type)
        frame.enter_scope(True)
        
        func_type = FunctionType([], return_type)
        self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        frame.get_new_index() 
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))

        # [FIX 1]: GỌI SUPER DISPOSE TRƯỚC (Parent First)
        if self.parent_name and self.parent_name != "java/lang/Object":
             self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), 0, frame))
             self.emit.print_out(self.emit.emit_invoke_special(
                 frame, 
                 f"{self.parent_name}/{method_name}", 
                 func_type
             ))

        # [FIX 1]: SAU ĐÓ MỚI CHẠY BODY CỦA CON (Child Last)
        this_sym = Symbol("this", ClassType(self.current_class), Index(0))
        env = [this_sym]
        body_access = Access(frame, env, False, True)
        
        self.visit(node.body, body_access)
        
        self.emit.print_out(self.emit.emit_return(return_type, frame))
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()

    def visit_parameter(self, node: "Parameter", o: Any = None):
        """
        Visit parameter - register parameter in frame.
        """
        # This is handled in generate_method
        pass

    def generate_method(self, node: "MethodDecl", frame: Frame, is_static: bool):
        """
        Generate code for a method.
        Handles method signature, parameter processing, super() injection, and body generation.
        """
        class_name = self.current_class
        method_name = node.name
        
        # ---------------------------------------------------------
        # 1. Build Method Signature
        # ---------------------------------------------------------
        param_types = [p.param_type for p in node.params]
        return_type = node.return_type

        # Special handling for 'main' method signature
        is_main = (method_name == "main" and len(param_types) == 0 and is_static and is_void_type(return_type))
        if is_main:
            param_types = [ArrayType(PrimitiveType("string"), 0)]
        
        func_type = FunctionType(param_types, return_type)
        
        # Emit the .method directive
        self.emit.print_out(
            self.emit.emit_method(
                method_name,
                func_type,
                is_static
            )
        )
        
        # ---------------------------------------------------------
        # 2. Setup Scope and Labels
        # ---------------------------------------------------------
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        # ---------------------------------------------------------
        # 3. Process Parameters & Build Symbol Table
        # ---------------------------------------------------------
        sym_list = []
        
        # A. Handle 'this' for Instance Methods
        if not is_static:
            # 'this' is always at index 0 for instance methods
            this_idx = frame.get_new_index()
            self.emit.print_out(self.emit.emit_var(this_idx, "this", ClassType(class_name), from_label, to_label))
            sym_list.append(Symbol("this", ClassType(class_name), Index(this_idx)))
            
        elif is_main: 
            # Static Main: 'args' is implicitly at index 0
            frame.get_new_index() 

        # B. Handle Explicit Parameters
        for i, param in enumerate(node.params):
            idx = frame.get_new_index()
            
            # Emit .var directive (for debugger/local var table)
            self.emit.print_out(self.emit.emit_var(idx, param.name, param.param_type, from_label, to_label))
            
            # CRITICAL: Add parameter to sym_list so visit_identifier can find it!
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))
        
        # Emit Start Label (Code execution starts here)
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # ---------------------------------------------------------
        # 4. Inject super() call for Constructors
        # ---------------------------------------------------------
        if method_name == "<init>":
            # 1. Load 'this' (Index 0)
            self.emit.print_out(self.emit.emit_read_var("this", ClassType(class_name), 0, frame))
            
            # 2. Call java.lang.Object.<init>()
            # We must use a Void function type because super() returns nothing
            super_init_type = FunctionType([], VoidType())
            self.emit.print_out(self.emit.emit_invoke_special(frame, "java/lang/Object/<init>", super_init_type))

        # ---------------------------------------------------------
        # 5. Generate Method Body
        # ---------------------------------------------------------
        # Pass the fully populated sym_list to the body context
        o = SubBody(frame, sym_list)
        self.visit(node.body, o)
        
        # ---------------------------------------------------------
        # 6. Epilog (Return & End)
        # ---------------------------------------------------------
        # Emit implicit return for void methods (constructors are void)
        if is_void_type(return_type):
            self.emit.print_out(self.emit.emit_return(return_type, frame))
        
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()

    # ============================================================================
    # Type System
    # ============================================================================

    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    def visit_class_type(self, node: "ClassType", o: Any = None):
        pass

    def visit_reference_type(self, node: "ReferenceType", o: Any = None):
        pass

    # ============================================================================
    # Statements
    # ============================================================================

    def visit_block_statement(self, node: "BlockStatement", o: SubBody = None):
        """
        Visit block statement - process variable declarations and statements.
        """
        if o is None: return
        
        o.frame.enter_scope(False)
        self.emit.print_out(self.emit.emit_label(o.frame.get_start_label(), o.frame))
        
        local_sym = o.sym[:]
        local_objects_to_destroy = [] # List biến cần hủy

        def has_destructor(class_name):
            current_name = class_name
            while current_name and current_name != "java/lang/Object":
                c_node = next((c for c in self.list_class if c.name == current_name), None)
                if not c_node: break
                for m in c_node.members:
                    if isinstance(m, DestructorDecl): return True
                current_name = c_node.superclass
            return False

        # Process Declarations
        for var_decl in node.var_decls:
            self.visit(var_decl, SubBody(o.frame, local_sym))
            for variable in var_decl.variables:
                sym = next((s for s in local_sym if s.name == variable.name), None)
                if sym and isinstance(var_decl.var_type, ClassType):
                    if has_destructor(var_decl.var_type.class_name):
                        local_objects_to_destroy.append(sym)
            
        # Process Statements
        for stmt in node.statements:
            self.visit(stmt, SubBody(o.frame, local_sym))
            
        # [FIX 2]: HỦY THEO THỨ TỰ KHAI BÁO (FIFO) - BỎ REVERSED
        # Test case yêu cầu: b (Shape) hủy trước c (Rectangle)
        for sym in local_objects_to_destroy:
            idx = sym.value.value 
            
            # a. Load Variable
            self.emit.print_out(self.emit.emit_read_var(
                sym.name, sym.type, idx, o.frame
            ))
            
            # b. Call dispose
            method_lexeme = f"{sym.type.class_name}/dispose"
            self.emit.print_out(self.emit.emit_invoke_virtual(
                method_lexeme,
                FunctionType([], VoidType), 
                o.frame
            ))

        self.emit.print_out(self.emit.emit_label(o.frame.get_end_label(), o.frame))
        o.frame.exit_scope()

    def visit_variable_decl(self, node: "VariableDecl", o: SubBody = None):
        """
        Visit variable declaration (e.g., int a, b = 5;)
        """
        frame = o.frame
        
        # Iterate over the list of variables in this declaration
        for var_node in node.variables:
            # 1. Allocate Index
            idx = frame.get_new_index()
            
            # 2. Emit .var directive (defines scope of the variable)
            self.emit.print_out(self.emit.emit_var(
                idx, 
                var_node.name, 
                node.var_type, 
                frame.get_start_label(), 
                frame.get_end_label()
            ))
            
            # 3. Handle Initialization (if exists)
            if var_node.init_value:
                # Generate code for the RHS expression
                # Note: We pass o.sym so initialization can refer to previous variables
                code, init_type = self.visit(var_node.init_value, Access(frame, o.sym, False))
                self.emit.print_out(code)
                
                # Handle Coercion (Int -> Float)
                if check_type(node.var_type, "float") and check_type(init_type, "int"):
                    self.emit.print_out(self.emit.emit_i2f(frame))
                    
                # Store the value into the variable
                self.emit.print_out(self.emit.emit_write_var(
                    var_node.name, node.var_type, idx, frame
                ))

            # -------------------------------------------------------------
            # 4. CRITICAL FIX: Add to Symbol Table
            # -------------------------------------------------------------
            # This ensures that subsequent statements know 'var_node.name' exists
            # and is located at 'idx'.
            o.sym.insert(0, Symbol(var_node.name, node.var_type, Index(idx)))

    def visit_variable(self, node: "Variable", o: Any = None):
        pass

    def visit_assignment_statement(self, node: "AssignmentStatement", o: SubBody = None):
        """
        Visit assignment statement - generate assignment code.
        """
        if o is None:
            return
        
        if type(node.lhs) is IdLHS:
            # Generate code for RHS
            code, typ = self.visit(node.rhs, Access(o.frame, o.sym))
            self.emit.print_out(code)
            
            # Generate code for LHS
            lhs_code, lhs_type = self.visit(node.lhs, Access(o.frame, o.sym, is_left=True))
            # 3. Handle Type Coercion (Int -> Float)
            if check_type(lhs_type, "float") and check_type(typ, "int"):
                self.emit.print_out(self.emit.emit_i2f(o.frame))

            self.emit.print_out(lhs_code)
        else:
            self.rhs = node.rhs

            ## TODO 1          
            lhs_code, _ = self.visit(node.lhs, Access(o.frame, o.sym, True))
            self.emit.print_out(lhs_code)
            self.rhs = None

    def visit_if_statement(self, node: "IfStatement", o: SubBody = None):
        """
        Visit if statement.
        TODO 3: Implement if statement code generation
        """
        """
        Visit if statement.
        Structure:
            [Condition Code]
            IfFalse(Label_Else)
            [Then Stmt]
            Goto(Label_Exit)
        Label_Else:
            [Else Stmt] (optional)
        Label_Exit:
        """
        frame = o.frame
        sym = o.sym
        
        # 1. Generate Labels
        label_else = frame.get_new_label()
        label_exit = frame.get_new_label()
        
        # 2. Generate Condition Code
        # Access(frame, sym, False) -> False means read-only access
        cond_code, _ = self.visit(node.condition, Access(frame, sym, False))
        self.emit.print_out(cond_code)
        
        # 3. Emit Jump Instruction
        # If the condition (top of stack) is FALSE (0), jump to label_else
        self.emit.print_out(self.emit.emit_if_false(label_else, frame))
        
        # 4. Visit 'Then' Statement
        self.visit(node.then_stmt, o)
        
        # 5. Jump to Exit (skip the else block)
        # Only needed if there is an else block, but safe to always have for uniformity
        if node.else_stmt:
            self.emit.print_out(self.emit.emit_goto(label_exit, frame))
        
        # 6. Label Else
        self.emit.print_out(self.emit.emit_label(label_else, frame))
        
        # 7. Visit 'Else' Statement (if exists)
        if node.else_stmt:
            self.visit(node.else_stmt, o)
            # 8. Label Exit
            self.emit.print_out(self.emit.emit_label(label_exit, frame))
        else:
            # If no else block, label_else IS the exit point, so we are done.
            # (label_exit is unused in this case, which is fine)
            pass

    def visit_for_statement(self, node: "ForStatement", o: Any = None):
        """
        Visit for statement.
        TODO 3: Implement for statement code generation
        """
        """
        Visit for statement (Pascal-style).
        Logic:
           var := start_expr
           L_Start:
               if (var > end_expr) goto L_Exit  (if 'to')
               [Body]
           L_Continue:
               var = var + 1
               goto L_Start
           L_Exit:
        """
        frame = o.frame
        sym = o.sym
        
        # 1. Retrieve the Loop Variable Symbol
        # The variable must already be declared in the scope (or outer scope)
        loop_var_sym = next((s for s in sym if s.name == node.variable), None)
        if not loop_var_sym:
            raise IllegalOperandException(f"Undeclared loop variable: {node.variable}")
            
        # 2. Init: var := start_expr
        # Generate code for Start Expression
        start_code, start_type = self.visit(node.start_expr, Access(frame, sym, False))
        self.emit.print_out(start_code)
        
        # Coercion Check (Int -> Float) if needed
        # (Assuming loop variables are usually Int, but checking to be safe)
        is_var_float = isinstance(loop_var_sym.type, PrimitiveType) and loop_var_sym.type.type_name == "float"
        is_val_int   = isinstance(start_type, PrimitiveType) and start_type.type_name == "int"
        
        if is_var_float and is_val_int:
            self.emit.print_out(self.emit.emit_i2f(frame))
            
        # Store result into the Loop Variable
        self.emit.print_out(self.emit.emit_write_var(
            loop_var_sym.name, loop_var_sym.type, loop_var_sym.value.value, frame
        ))
        
        # 3. Setup Loop Labels
        frame.enter_loop()
        loop_start_label = frame.get_new_label()   # Check condition here
        exit_label = frame.get_break_label()       # Jump here to stop
        continue_label = frame.get_continue_label() # Jump here to update (continue stmt)
        
        # 4. Loop Start (Condition Check)
        self.emit.print_out(self.emit.emit_label(loop_start_label, frame))
        
        # A. Load Loop Variable
        self.emit.print_out(self.emit.emit_read_var(
            loop_var_sym.name, loop_var_sym.type, loop_var_sym.value.value, frame
        ))
        
        # B. Load End Expression
        end_code, end_type = self.visit(node.end_expr, Access(frame, sym, False))
        self.emit.print_out(end_code)
        
        # C. Compare and Jump
        # If 'to' (Ascending): Exit if var > end
        # If 'downto' (Descending): Exit if var < end
        if node.direction == "to":
            self.emit.print_out(self.emit.emit_ificmpgt(exit_label, frame))
        else: # downto
            self.emit.print_out(self.emit.emit_ificmplt(exit_label, frame))
            
        # 5. Visit Body
        self.visit(node.body, o)
        
        # 6. Update (Continue Label)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        
        # Load var
        self.emit.print_out(self.emit.emit_read_var(
            loop_var_sym.name, loop_var_sym.type, loop_var_sym.value.value, frame
        ))
        # Push 1
        self.emit.print_out(self.emit.emit_push_iconst(1, frame))
        
        # Add or Sub
        if node.direction == "to":
            self.emit.print_out(self.emit.emit_add_op("+", loop_var_sym.type, frame))
        else:
            self.emit.print_out(self.emit.emit_add_op("-", loop_var_sym.type, frame))
            
        # Store back
        self.emit.print_out(self.emit.emit_write_var(
            loop_var_sym.name, loop_var_sym.type, loop_var_sym.value.value, frame
        ))
        
        # Jump back to start
        self.emit.print_out(self.emit.emit_goto(loop_start_label, frame))
        
        # 7. Exit Label
        self.emit.print_out(self.emit.emit_label(exit_label, frame))
        frame.exit_loop()

    def visit_break_statement(self, node: "BreakStatement", o: Any = None):
        """
        Visit break statement.
        TODO 3: Implement break statement code generation
        """
        frame = o.frame
        # Retrieve the current break label from the stack
        break_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_goto(break_label, frame))

    def visit_continue_statement(self, node: "ContinueStatement", o: SubBody = None):
        """
        Visit continue statement.
        TODO 3: Implement continue statement code generation
        """
        frame = o.frame
        # Retrieve the current continue label from the stack
        # (For 'while', this is the condition; For 'for', this is the update)
        continue_label = frame.get_continue_label()
        self.emit.print_out(self.emit.emit_goto(continue_label, frame))

    def visit_return_statement(self, node: "ReturnStatement", o: SubBody = None):
        """
        Visit return statement - generate return code.
        """
        if o is None:
            return
        
        # Generate code for return value
        code, typ = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(code)
        
        # Emit return instruction
        self.emit.print_out(self.emit.emit_return(typ, o.frame))

    def visit_method_invocation_statement(
        self, node: "MethodInvocationStatement", o: Any = None
    ):
        """
        Visit method invocation statement.
        """
        # TODO 1: Implement method invocation statement
        # 1. Setup Context
        frame = o.frame
        symbol = o.sym
        
        # 2. Delegate to the Expression Visitor
        # node.method_call is a PostfixExpression (or CallExpr).
        # Calling visit() on it will generate all the code:
        #   - Determine Static vs Virtual
        #   - Load Object
        #   - Load Args (with coercion)
        #   - Invoke Method
        #   - Return the Method's return type
        code, ret_type = self.visit(node.method_call, o)
        self.emit.print_out(code)
        
        # 3. Stack Cleanup
        # Since this is a STATEMENT, the stack must be empty after it finishes.
        # If the method returns a value (e.g., int, float, object), we must POP it.
        # If the method returns void, there is nothing to pop.
        if not is_void_type(ret_type):
            self.emit.print_out(self.emit.emit_pop(frame))

    # ============================================================================
    # Left-hand Side (LHS)
    # ============================================================================

    def visit_id_lhs(self, node: "IdLHS", o: Any = None):
        """
        Visit identifier LHS - generate code to write to variable.
        """
        if o is None:
            return "", None
        
        # Find symbol
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared variable: {node.name}")
        
        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            return code, sym.type
        else:
            raise IllegalOperandException(f"Cannot assign to: {node.name}")
        
    def lookup_field(self, class_name: str, field_name: str):
        """
        Tìm kiếm thông tin về Field (Attribute) trong Class hiện tại và các Class cha.
        Trả về node Attribute đã được gắn thêm thông tin .attr_type và .is_static.
        """
        current_class_name = class_name
        
        while current_class_name:
            # 1. Tìm ClassDecl trong danh sách đã đăng ký
            class_decl = next((c for c in self.list_class if c.name == current_class_name), None)
            
            if not class_decl:
                # Nếu không tìm thấy class (hoặc đã lên đến Object mà hết), dừng lại.
                break 
            
            # 2. Duyệt qua từng thành viên trong Class
            for mem in class_decl.members:
                # Chỉ quan tâm đến AttributeDecl (Khai báo thuộc tính)
                if isinstance(mem, AttributeDecl):
                    
                    # -----------------------------------------------------------
                    # LOGIC QUAN TRỌNG: Lấy Type từ khai báo cha (AttributeDecl)
                    # -----------------------------------------------------------
                    # Tùy thuộc vào cấu trúc AST của bạn, Type thường nằm ở 'mem.type' hoặc 'mem.decl.type'
                    
                    decl_type = None
                    is_static = False

                    # Cách lấy Type an toàn (Kiểm tra nhiều trường hợp AST)
                    if hasattr(mem, 'type'):
                        decl_type = mem.type
                    elif hasattr(mem, 'decl') and hasattr(mem.decl, 'var_type'):
                        decl_type = mem.decl.var_type
                    elif hasattr(mem, 'attr_type'): # Một số AST dùng tên này
                        decl_type = mem.attr_type
                        
                    # Cách lấy cờ Static
                    # Thường là mem.kind (nếu dùng Class MemberKind) hoặc mem.is_static
                    if hasattr(mem, 'kind'):
                        # Giả sử Static là một Class hoặc Enum, kiểm tra tên
                        is_static = str(mem.kind) == "Static" or isinstance(mem.kind, Static)
                    elif hasattr(mem, 'is_static'):
                        is_static = mem.is_static

                    # -----------------------------------------------------------
                    # 3. Tìm tên Field trong danh sách thuộc tính con
                    # -----------------------------------------------------------
                    # Trường hợp A: AttributeDecl chứa list các Attribute (VD: int a, b, c;)
                    if hasattr(mem, 'attributes'):
                        for attr in mem.attributes:
                            if attr.name == field_name:
                                # FOUND!
                                # Inject (Tiêm) Type và Static vào node con để trả về
                                attr.attr_type = decl_type
                                attr.is_static = is_static
                                return attr
                                
                    # Trường hợp B: AttributeDecl chứa 1 VariableDecl duy nhất
                    elif hasattr(mem, 'decl') and isinstance(mem.decl, VariableDecl):
                        if mem.decl.variable == field_name:
                            # FOUND!
                            mem.decl.attr_type = decl_type
                            mem.decl.is_static = is_static
                            return mem.decl

            # 4. Nếu không tìm thấy ở class này, leo lên class cha
            current_class_name = class_decl.superclass if class_decl.superclass else None
            
        return None

    def visit_postfix_lhs(self, node: "PostfixLHS", o: Access = None):
        """
        Visit postfix LHS (e.g. a.b := 5 or arr[0] := 5).
        Generates code for the Left-Hand Side of an assignment.
        """
        """
        Visit postfix LHS (e.g. a.b := 5 or arr[0] := 5).
        """
        postfix_expr = node.postfix_expr
        primary = postfix_expr.primary
        ops = postfix_expr.postfix_ops
        
        if not ops:
            return "", None

        current_type = None

        # ---------------------------------------------------------
        # 1. Process PRIMARY (Base Object)
        # ---------------------------------------------------------
        if isinstance(primary, ThisExpression):
            code, current_type = self.visit(primary, Access(o.frame, o.sym, False))
            self.emit.print_out(code)
            
        elif isinstance(primary, Identifier):
            sym = next(filter(lambda s: s.name == primary.name, o.sym), None)
            if sym:
                # Handle 'mtype' vs 'type' attribute inconsistency
                sym_type = getattr(sym, 'mtype', getattr(sym, 'type', None))
                self.emit.print_out(self.emit.emit_read_var(
                    sym.name, sym_type, sym.value.value, o.frame
                ))
                current_type = sym_type
            else:
                # Static Access (Class Name)
                current_type = ClassType(primary.name)
        
        else:
            code, current_type = self.visit(primary, Access(o.frame, o.sym, False))
            self.emit.print_out(code)

        # ---------------------------------------------------------
        # 2. Process INTERMEDIATE Operations (Reads/Loads)
        # ---------------------------------------------------------
        for i in range(len(ops) - 1):
            op = ops[i]
            
            if isinstance(op, MemberAccess):
                class_name = current_type.class_name
                field = self.lookup_field(class_name, op.member_name)
                
                if field.is_static:
                    self.emit.print_out(self.emit.emit_get_static(
                        class_name + "/" + op.member_name, field.attr_type, o.frame
                    ))
                else:
                    self.emit.print_out(self.emit.emit_get_field(
                        class_name + "/" + op.member_name, field.attr_type, o.frame
                    ))
                current_type = field.attr_type
                
            elif isinstance(op, ArrayAccess):
                # FIX: Use op.index
                idx_code, _ = self.visit(op.index, Access(o.frame, o.sym, False))
                self.emit.print_out(idx_code)
                
                elem_type = current_type.element_type
                self.emit.print_out(self.emit.emit_aload(elem_type, o.frame))
                current_type = elem_type

        # ---------------------------------------------------------
        # 3. Process LAST Operation (The STORE/WRITE)
        # ---------------------------------------------------------
        last_op = ops[-1]
        
        if isinstance(last_op, MemberAccess):
            class_name = current_type.class_name
            field = self.lookup_field(class_name, last_op.member_name)
            
            # A. Generate RHS Code
            rhs_code, rhs_type = self.visit(self.rhs, Access(o.frame, o.sym, False))
            self.emit.print_out(rhs_code)
            
            # B. Coercion
            # Calls global check_type
            lhs_is_float = check_type(field.attr_type, "float")
            rhs_is_int = check_type(rhs_type, "int")

            if lhs_is_float and rhs_is_int:
                self.emit.print_out(self.emit.emit_i2f(o.frame))
            
            # C. Store
            if field.is_static:
                self.emit.print_out(self.emit.emit_put_static(
                    class_name + "/" + last_op.member_name, field.attr_type, o.frame
                ))
            else:
                self.emit.print_out(self.emit.emit_put_field(
                    class_name + "/" + last_op.member_name, field.attr_type, o.frame
                ))
                
        elif isinstance(last_op, ArrayAccess):
            # A. Generate Index Code
            # FIX: Use last_op.index
            idx_code, _ = self.visit(last_op.index, Access(o.frame, o.sym, False))
            self.emit.print_out(idx_code)
            
            # B. Generate RHS Code
            rhs_code, rhs_type = self.visit(self.rhs, Access(o.frame, o.sym, False))
            self.emit.print_out(rhs_code)
            
            # C. Coercion
            elem_type = current_type.element_type
            lhs_is_float = check_type(elem_type, "float")
            rhs_is_int = check_type(rhs_type, "int")

            if lhs_is_float and rhs_is_int:
                self.emit.print_out(self.emit.emit_i2f(o.frame))
                
            # D. Store
            self.emit.print_out(self.emit.emit_astore(elem_type, o.frame))
            
        return "", None

    # ============================================================================
    # Expressions
    # ============================================================================

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        op = node.operator  # Check if your AST uses .op or .operator
        
        # GROUP 1: ARITHMETIC & RELATIONAL
        if op in ['+', '-', '*', '/', '\\', '%', '>', '<', '>=', '<=', '==', '!=']:
            lhs_code, lhs_type = self.visit(node.left, o)
            rhs_code, rhs_type = self.visit(node.right, o)
            
            is_float_op = check_type(lhs_type, "float") or check_type(rhs_type, "float")
            
            code = lhs_code
            if is_float_op and check_type(lhs_type, "int"):
                code += self.emit.emit_i2f(o.frame)
                
            code += rhs_code
            if is_float_op and check_type(rhs_type, "int"):
                code += self.emit.emit_i2f(o.frame)
            
            # Xử lý Arithmetic
            if op in ['+', '-', '*', '/', '\\', '%']:
                if op in ['>', '<', '>=', '<=', '==', '!=']: pass # Skip relational logic here
                else:
                    result_type = FloatType if is_float_op else IntType
                    if op in ['+', '-']:
                        code += self.emit.emit_add_op(op, result_type, o.frame)
                    elif op == '*':
                        code += self.emit.emit_mul_op(op, result_type, o.frame)
                    elif op == '/':
                        if is_float_op: code += self.emit.jvm.emitFDIV()
                        else: code += self.emit.jvm.emitIDIV()
                    elif op == '\\':
                         code += self.emit.jvm.emitIDIV()
                         result_type = IntType
                    elif op == '%':
                        code += self.emit.emit_mod(o.frame)
                    return code, result_type

            # Xử lý Relational (Else của arithmetic ops logic trên)
            # [FIXED SECTION HERE]
            compare_type = FloatType if is_float_op else IntType
            code += self.emit.emit_re_op(op, compare_type, o.frame)
            return code, BoolType

        # GROUP 2: LOGICAL AND (&&)
        elif op == '&&':
            # ... (Giữ nguyên code && đã đúng ở câu trả lời trước) ...
            # Code ngắn gọn để reference:
            label_false = o.frame.get_new_label()
            label_end = o.frame.get_new_label()
            code = ""
            l_c, _ = self.visit(node.left, o)
            code += l_c + self.emit.emit_if_false(label_false, o.frame)
            r_c, _ = self.visit(node.right, o)
            code += r_c + self.emit.emit_if_false(label_false, o.frame)
            code += self.emit.emit_push_iconst(1, o.frame)
            code += self.emit.emit_goto(label_end, o.frame)
            code += self.emit.emit_label(label_false, o.frame)
            code += self.emit.emit_push_iconst(0, o.frame)
            code += self.emit.emit_label(label_end, o.frame)
            return code, BoolType

        # GROUP 3: LOGICAL OR (||)
        elif op == '||':
            # ... (Giữ nguyên code || đã đúng ở câu trả lời trước) ...
            # Code ngắn gọn để reference:
            label_true = o.frame.get_new_label()
            label_end = o.frame.get_new_label()
            code = ""
            l_c, _ = self.visit(node.left, o)
            code += l_c + self.emit.emit_if_true(label_true, o.frame)
            r_c, _ = self.visit(node.right, o)
            code += r_c + self.emit.emit_if_true(label_true, o.frame)
            code += self.emit.emit_push_iconst(0, o.frame)
            code += self.emit.emit_goto(label_end, o.frame)
            code += self.emit.emit_label(label_true, o.frame)
            code += self.emit.emit_push_iconst(1, o.frame)
            code += self.emit.emit_label(label_end, o.frame)
            return code, BoolType

        return "", None

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        """
        Visit unary operation.
        TODO 2: Implement unary operation code generation
        """
        op = node.operator
        
        # 1. Visit the Operand
        code, typ = self.visit(node.operand, o)
        
        # 2. Emit Logic based on Operator
        if op == '-':
            # Negation (Arithmetic)
            if isinstance(typ, PrimitiveType) and typ.type_name == "float":
                code += self.emit.jvm.emitFNEG()
            else:
                code += self.emit.jvm.emitINEG()
                
        elif op == '!':
            # Logical Not (Boolean) using Jump Logic
            # Goal: Input 1 -> Output 0; Input 0 -> Output 1
            
            label_was_true = o.frame.get_new_label()
            label_end = o.frame.get_new_label()
            
            # Stack: [Value]
            # Nếu Value là True (1), nhảy đến nơi xử lý trả về 0
            code += self.emit.emit_if_true(label_was_true, o.frame)
            
            # --- Trường hợp Value là False (0) ---
            # Ta push 1 (Kết quả của !False là True)
            code += self.emit.emit_push_iconst(1, o.frame)
            code += self.emit.emit_goto(label_end, o.frame)
            
            # --- Trường hợp Value là True (1) ---
            code += self.emit.emit_label(label_was_true, o.frame)
            code += self.emit.emit_push_iconst(0, o.frame)
            
            # --- Kết thúc ---
            code += self.emit.emit_label(label_end, o.frame)
            
        return code, typ

    def lookup_method(self, class_name: str, method_name: str):
        """Helper to find a method in a class (or its parents)."""
        class_decl = next((c for c in self.list_class if c.name == class_name), None)
        if not class_decl: return None

        for member in class_decl.members:
            if isinstance(member, MethodDecl) and member.name == method_name:
                return member

        if class_decl.superclass:
            return self.lookup_method(class_decl.superclass, method_name)
        return None

    def visit_postfix_expression(self, node: "PostfixExpression", o: Access = None):
        """
        Visit postfix expression.
        Assumes 'o' is a valid Access object containing .frame and .sym.
        """
        frame = o.frame
        sym = o.sym
        
        primary = node.primary
        ops = node.postfix_ops
        
        code = ""
        current_type = None
        is_static_access = False
        
        # ---------------------------------------------------------
        # 1. Process PRIMARY (Base)
        # ---------------------------------------------------------
        
        if isinstance(primary, ThisExpression):
            # Delegate to visit_this_expression
            c, t = self.visit(primary, o)
            code += c
            current_type = t
            
        elif isinstance(primary, Identifier):
            # Try to find the identifier in the local symbol table
            found = next(filter(lambda s: s.name == primary.name, sym), None)
            
            if found:
                # Found Variable -> Instance Access (e.g. 'a' or 'this')
                # Generate code to read the variable
                c = self.emit.emit_read_var(found.name, found.type, found.value.value, frame)
                code += c
                current_type = found.type
            else:
                # Not Found -> Assume it is a Class Name (e.g. 'Math')
                # Do NOT generate load code (you can't load a class name)
                current_type = ClassType(primary.name)
                is_static_access = True
                
        else:
            # Complex Primary (e.g. (expr) or new A())
            c, t = self.visit(primary, o)
            code += c
            current_type = t

        # ---------------------------------------------------------
        # 2. Process Operations Chain (Method Calls, Field Access, Arrays)
        # ---------------------------------------------------------
        
        for op in ops:
            # We pass a tuple context to the specific visitors:
            # (Access Object, Type of previous element, Is it a static class name?)
            context = (o, current_type, is_static_access)
            
            op_code, op_type = self.visit(op, context)
            
            code += op_code
            current_type = op_type
            
            # After the first operation (like .field or .method()), 
            # the result is definitely a value/reference, not a Class Name.
            is_static_access = False 
            
        return code, current_type

    def visit_method_call(self, node: "MethodCall", o: Access = None):
        """
        Visit method call.
        TODO: Implement method call code generation
        """
        access, parent_type, is_static = o
        frame = access.frame
        
        class_name = parent_type.class_name
        method = self.lookup_method(class_name, node.method_name)
        
        if not method:
            raise IllegalOperandException(node.method_name)
            
        # 1. Generate Argument Code
        code = ""
        param_types = [p.param_type for p in method.params]
        
        for i, arg in enumerate(node.args):
            arg_code, arg_type = self.visit(arg, access)
            code += arg_code
            
            # Handle Coercion (Int -> Float)
            if isinstance(param_types[i], PrimitiveType) and param_types[i].type_name == "float" and isinstance(arg_type, PrimitiveType) and arg_type.type_name == "int":
                code += self.emit.emit_i2f(frame)

        # 2. Invoke Method
        func_type = FunctionType(param_types, method.return_type)
        method_lexeme = class_name + "/" + node.method_name
        
        if is_static:
            if not method.is_static:
                raise IllegalOperandException(node.method_name)
            code += self.emit.emit_invoke_static(method_lexeme, func_type, frame)
        else:
            code += self.emit.emit_invoke_virtual(method_lexeme, func_type, frame)
            
        return code, method.return_type

    def visit_member_access(self, node: "MemberAccess", o: Access = None):
        """
        Visit member access (RHS) - e.g., b.b
        """
        # 1. Unpack Context
        if isinstance(o, tuple):
             access, parent_type, is_static_access = o
             frame = access.frame
        else:
             # Should not happen in correct visitor chain
             return "", None 

        class_name = parent_type.class_name
        
        # 2. Lookup Field
        field = self.lookup_field(class_name, node.member_name)
        
        if not field:
            raise IllegalOperandException(node.member_name)

        # 3. Generate Code
        # field.attr_type and field.is_static are now available thanks to lookup_field logic
        
        if field.is_static:
            code = self.emit.emit_get_static(f"{class_name}/{node.member_name}", field.attr_type, frame)
        else:
            code = self.emit.emit_get_field(f"{class_name}/{node.member_name}", field.attr_type, frame)
            
        return code, field.attr_type

    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        """
        Visit array access.
        TODO: Implement array access code generation
        """
        """
        Visit array access.
        """
        # Unpack context
        access, parent_type, is_static = o
        frame = access.frame
        
        if is_static:
            raise IllegalOperandException("Cannot index a Class Name")
            
        # 1. Generate Index Code
        # FIX: Use node.index instead of node.expr
        idx_code, _ = self.visit(node.index, access)
        
        # 2. Emit Load Instruction
        elem_type = parent_type.element_type
        load_code = self.emit.emit_aload(elem_type, frame)
        
        return idx_code + load_code, elem_type

    def visit_object_creation(self, node: "ObjectCreation", o: Access = None):
        class_name = node.class_name
        
        # 1. Allocate Memory
        code = self.emit.jvm.emitNEW(class_name)
        o.frame.push() # Push Ref
        code += self.emit.emit_dup(o.frame) # Stack: [Ref, Ref]
        
        # 2. Find the MATCHING Constructor Definition in AST
        constructor = None
        for c in self.list_class:
            if c.name == class_name:
                for m in c.members:
                    if isinstance(m, ConstructorDecl):
                        # [FIX BUG]: Kiểm tra số lượng tham số phải khớp với số lượng args
                        if len(m.params) == len(node.args):
                            constructor = m
                            break
                if constructor: break
        
        # Default to empty if not found (default constructor)
        param_types = []
        if constructor:
            # Lưu ý: Kiểm tra lại attribute là 'var_type' hay 'param_type' tùy AST của bạn
            # Trong các câu trước bạn dùng param.var_type
            param_types = [p.param_type for p in constructor.params]
            
        # 3. Generate Code for Arguments
        for i, arg in enumerate(node.args):
            arg_code, arg_type = self.visit(arg, o)
            code += arg_code
            
            # Handle Coercion
            if i < len(param_types):
                req_type = param_types[i]
                def check_type(t, name):
                     return isinstance(t, PrimitiveType) and t.type_name == name
                     
                if check_type(req_type, "float") and check_type(arg_type, "int"):
                    code += self.emit.emit_i2f(o.frame)

        # 4. Invoke Special
        func_type = FunctionType(param_types, VoidType)
        method_lexeme = class_name + "/<init>"
        
        code += self.emit.emit_invoke_special(o.frame, method_lexeme, func_type)
        
        # Stack sau invoke: [Ref] (đúng ý đồ để gán vào biến)
        return code, ClassType(class_name)


    def visit_identifier(self, node: "Identifier", o: Access = None):
        """
        Visit identifier - generate code to read variable.
        """
        if o is None:
            return "", None
        
        # 1. Find symbol
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        
        if sym is None:
            # If we are here, 'a' is not in o.sym -> generate_method failed to add it
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")
        
        # 2. Get Type Safely (Handle sym.mtype vs sym.type)
        sym_type = getattr(sym, 'mtype', getattr(sym, 'type', None))
        
        # 3. Generate Code
        if isinstance(sym.value, Index):
            # Generate Read Code (iload, fload, aload)
            code = self.emit.emit_read_var(
                sym.name, 
                sym_type, 
                sym.value.value, 
                o.frame
            )
            return code, sym_type
        else:
            # Likely a Class Name or invalid symbol
            raise IllegalOperandException(f"Cannot read: {node.name}")

    def visit_this_expression(self, node: "ThisExpression", o: Access = None):
        """
        Visit this expression - load 'this' reference.
        """
        if o is None:
            return "", None
        
        # Find 'this' in symbol table (should be at index 0 for instance methods)
        this_sym = next(filter(lambda x: x.name == "this", o.sym), None)
        if this_sym is None:
            raise IllegalOperandException("'this' not available in static context")
        
        if type(this_sym.value) is Index:
            code = self.emit.emit_read_var(
                "this", this_sym.type, this_sym.value.value, o.frame
            )
            return code, ClassType(self.current_class)
        else:
            raise IllegalOperandException("Invalid 'this' reference")

    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Access = None
    ):
        """
        Visit parenthesized expression - just visit inner expression.
        """
        return self.visit(node.expr, o)

    # ============================================================================
    # Literals
    # ============================================================================

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        """
        Visit integer literal - push integer constant.
        """
        if o is None:
            return "", None
        # Fix: Check if o is already a Frame, otherwise get .frame
        frame = o if isinstance(o, Frame) else o.frame
        code = self.emit.emit_push_iconst(node.value, frame)
        return code, IntType

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        """
        Visit float literal - push float constant.
        """
        if o is None:
            return "", None
        # Fix: Check if o is already a Frame, otherwise get .frame
        frame = o if isinstance(o, Frame) else o.frame
        code = self.emit.emit_push_fconst(str(node.value), frame)
        return code, FloatType

    def visit_bool_literal(self, node: "BoolLiteral", o: Any = None):
        """
        Visit boolean literal - push boolean constant.
        """
        if o is None:
            return "", None
        # Fix: Check if o is already a Frame, otherwise get .frame
        frame = o if isinstance(o, Frame) else o.frame
        value_str = "true" if node.value else "false"
        code = self.emit.emit_push_iconst(value_str, frame)
        return code, BoolType

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        """
        Visit string literal - push string constant.
        """
        if o is None:
            return "", None
        # Fix: Check if o is already a Frame, otherwise get .frame
        frame = o if isinstance(o, Frame) else o.frame
        code = self.emit.emit_push_const('"' + node.value + '"', PrimitiveType("string"), frame)
        return code, StringType
    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None):
        """
        Visit array literal.
        TODO 2: Implement array literal code generation
        """
        """
        Visit array literal (e.g., {1, 2, 3}).
        """
        code = ""
        elements = node.value
        size = len(elements)
        
        # 1. Push Array Size
        code += self.emit.emit_push_iconst(size, o.frame)
        
        # Helper check_type nội bộ
        def check_type(t, name):
            return isinstance(t, PrimitiveType) and t.type_name == name

        # 2. Handle Empty Array (Default to int[])
        if size == 0:
            code += self.emit.emit_new_array("int")
            # [FIX FRAME] newarray pop size (1), push ref (1) -> Net change 0
            # Nhưng Emitter không update frame tự động, ta làm thủ công:
            o.frame.pop() # Pop Size
            o.frame.push() # Push ArrayRef
            return code, ArrayType(PrimitiveType("int"), 0)

        # 3. Visit First Element (Probe Type & Code)
        first_code, first_type = self.visit(elements[0], o)
        
        # [FIX FRAME 2]
        # visit() ở trên đã gọi frame.push(). 
        # Nhưng ta chưa emit first_code ngay, nên cần pop ra để trả frame về trạng thái [Size]
        o.frame.pop() 

        store_instr = ""
        
        # 4. Generate New Array Instruction
        if check_type(first_type, "int"):
            code += self.emit.emit_new_array("int")
            store_instr = self.emit.jvm.emitIASTORE()
        elif check_type(first_type, "float"):
            code += self.emit.emit_new_array("float")
            store_instr = self.emit.jvm.emitFASTORE()
        elif check_type(first_type, "boolean"):
            code += self.emit.emit_new_array("boolean")
            store_instr = self.emit.jvm.emitBASTORE() # Dùng bastore cho boolean
        elif check_type(first_type, "string"):
            # [FIX ANEWARRAY] Dùng tên class trần "java/lang/String"
            code += self.emit.jvm.emitANEWARRAY("java/lang/String")
            store_instr = self.emit.jvm.emitAASTORE()
        else:
            # Fallback cho Object Array khác
            type_desc = ""
            if isinstance(first_type, ClassType):
                type_desc = first_type.class_name
            else:
                type_desc = self.emit.get_jvm_type(first_type)
            code += self.emit.jvm.emitANEWARRAY(type_desc)
            store_instr = self.emit.jvm.emitAASTORE()

        # [FIX FRAME 3] Update Frame sau lệnh newarray/anewarray (Pop Size, Push Ref)
        o.frame.pop() 
        o.frame.push()

        # 5. Store First Element
        code += self.emit.emit_dup(o.frame)              # Stack: [Ref, Ref]
        code += self.emit.emit_push_iconst(0, o.frame)   # Stack: [Ref, Ref, 0]
        
        # Push lại Value vào frame (khớp với first_code sắp emit)
        o.frame.push()                                   # Stack: [Ref, Ref, 0, Value]
        code += first_code
        
        # (Không cần Coercion cho phần tử đầu vì nó định nghĩa kiểu mảng)

        code += store_instr
        # Pop 3 (Ref, Index, Value) khỏi frame
        o.frame.pop()
        o.frame.pop()
        o.frame.pop()

        # 6. Store Remaining Elements
        for i in range(1, size):
            elem_code, elem_type = self.visit(elements[i], o)
            # Tương tự: pop Value ra để push dup/index trước
            o.frame.pop() 
            
            code += self.emit.emit_dup(o.frame)
            code += self.emit.emit_push_iconst(i, o.frame)
            
            # Push Value lại
            o.frame.push() 
            code += elem_code
            
            # Coercion (Int -> Float)
            if check_type(first_type, "float") and check_type(elem_type, "int"):
                code += self.emit.emit_i2f(o.frame)
                
            code += store_instr
            # Pop 3 (Ref, Index, Value) khỏi frame
            o.frame.pop()
            o.frame.pop()
            o.frame.pop()
            
        return code, ArrayType(first_type, size)

    def visit_nil_literal(self, node: "NilLiteral", o: Access = None):
        """
        Visit nil literal - push null reference.
        """
        if o is None:
            return "", None
        o.frame.push()
        code = self.emit.jvm.emitPUSHNULL()
        return code, None  # Type will be determined by context
    
    def visit_method_invocation(self, node, o = None):
        return self.visit_method_call(node, o)
    def visit_static_member_access(self, node, o = None):
        return self.visit_member_access(node, o)
    def visit_static_method_invocation(self, node, o = None):
        return self.visit_method_call(node, o)