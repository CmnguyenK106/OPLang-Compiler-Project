"""
Static Semantic Checker for OPLang Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the OPLang object-oriented programming language. It performs type checking,
scope management, inheritance validation, and detects all semantic errors as 
specified in the OPLang language specification.
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ClassDecl, AttributeDecl, Attribute, MethodDecl,
    ConstructorDecl, DestructorDecl, Parameter, VariableDecl, Variable,
    AssignmentStatement, IfStatement, ForStatement, BreakStatement,
    ContinueStatement, ReturnStatement, MethodInvocationStatement,
    BlockStatement, PrimitiveType, ArrayType, ClassType, ReferenceType,
    IdLHS, PostfixLHS, BinaryOp, UnaryOp, PostfixExpression, PostfixOp,
    MethodCall, MemberAccess, ArrayAccess, ObjectCreation, Identifier,
    ThisExpression, ParenthesizedExpression, IntLiteral, FloatLiteral,
    BoolLiteral, StringLiteral, ArrayLiteral, NilLiteral, Type, Expr, Literal
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredClass,
    UndeclaredAttribute, UndeclaredMethod, CannotAssignToConstant,
    TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
    MustInLoop, IllegalConstantExpression, IllegalArrayLiteral,
    IllegalMemberAccess, NoEntryPoint
)

class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__()
        self.param_types = param_types
        self.return_type = return_type

    def accept(self, visitor, o=None):
        return visitor.visit_function_type(self, o)
    
class Symbol:
    def __init__(
        self,
        name: str,
        typ: 'Type',
        isFinal: bool = False,
        isStatic: bool = False,
        isAssigned: bool = False,
        method_type: Any = None
    ):
        self.name = name              # Tên của biến / hằng / hàm / class
        self.typ = typ                # Kiểu dữ liệu
        self.isFinal = isFinal        # Đánh dấu là hằng số (final)
        self.isStatic = isStatic      # Đánh dấu là static
        self.isAssigned = isAssigned  # Đã được gán giá trị hay chưa
        self.method_type = method_type    # Kiểu method if method

class StaticChecker(ASTVisitor):
    """
TODO task 1
    1. Redeclared - Variables, constants, attributes, classes, methods, parameters
    2. Undeclared - Identifiers, classes, attributes, methods 
    7. MustInLoop - Break/continue outside loop contexts
    Also checks for valid entry point: static void main() with no parameters.
TODO task 2
    3. CannotAssignToConstant - Assignment to final variables/attributes
    6. TypeMismatchInConstant - Type incompatibilities in constant declarations
    8. IllegalArrayLiteral - Invalid expressions in constant initialization
TODO task 3
    4. TypeMismatchInStatement - Type incompatibilities in statements
    5. TypeMismatchInExpression - Type incompatibilities in expressions
    6. TypeMismatchInConstant - Type incompatibilities in constant declarations
    10. IllegalMemberAccess - Improper access to static or instance members
    """
    def __init__(self):
        self.list_class: List[ClassDecl] = [
            ClassDecl("io", None, [
                # int
                MethodDecl(True, PrimitiveType("int"), "readInt", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeInt", [Parameter(PrimitiveType("int"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeIntLn", [Parameter(PrimitiveType("int"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("string"), "readStr", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeStr", [Parameter(PrimitiveType("string"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeStrLn", [Parameter(PrimitiveType("string"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("float"), "readFloat", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeFloat", [Parameter(PrimitiveType("float"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeFloatLn", [Parameter(PrimitiveType("float"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("boolean"), "readBool", [], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeBool", [Parameter(PrimitiveType("boolean"), "anArg")], BlockStatement([], [])),
                MethodDecl(True, PrimitiveType("void"), "writeBoolLn", [Parameter(PrimitiveType("boolean"), "anArg")], BlockStatement([], [])),

                # TODO
            ])
        ]
        self.method_curr: MethodDecl = None
        self.class_curr : ClassDecl = None
        self.loop = 0

    def check_program(self, ast):
        self.visit(ast) 

    def visit_program(self, node: "Program", o: Any = None):
        self.list_class += node.class_decls
        initial_global_scope = []
        for c in self.list_class:
            # Kiểm tra Redeclared Class ngay tại đây (Pass 1.5)
            found = next(filter(lambda sym: sym.name == c.name, initial_global_scope), None)
            if found:
                raise Redeclared("Class", c.name)
            initial_global_scope.append(Symbol(c.name, ClassType(c.name)))

        reduce(
            lambda acc_scope, class_decl: self.visit(
                class_decl,
                (acc_scope, [acc_scope]) # Pattern B: (current_global, full_env)
            ),
            node.class_decls,
            initial_global_scope
        )
        
        #reduce(lambda acc, class_decl: [self.visit(class_decl, acc)] + acc[1:], node.class_decls, [[Symbol("io", ClassType("io"))]])
        main_class = next(
            (c for c in node.class_decls if any(
                m.name == "main" and m.is_static and
                isinstance(m.return_type, PrimitiveType) and m.return_type.type_name == "void" and
                len(m.params) == 0
                for m in c.members if isinstance(m, MethodDecl)
            )),
            None
        )
        if not main_class:
            raise NoEntryPoint()


    def visit_class_decl(self, node: "ClassDecl", o: Any = None) -> list[Symbol]:
        """
        Visits a ClassDecl.
        'o' is a tuple: (current_global_scope, full_env)
        Returns the *new* updated global scope.
        """
    
        # 1. Unpack the context
        # 'global_scope' is the scope built so far (e.g., [Symbol('io'), Symbol('votien')])
        # 'full_env' is [[Symbol('io'), Symbol('votien')]]
        global_scope = o[0]
        global_env = o[1] 
    
        # 2. Set current class context (for 'this' and 'super')
        previous_class = self.class_curr
        self.class_curr = node
    
        try:
            # 5. Check for Superclass (Undeclared, Circular)
            if node.superclass:
                ancestors = set() 
                current_parent_name = node.superclass
            
                while current_parent_name:
                    # 5a. Check for circular inheritance
                    # if current_parent_name == node.name or current_parent_name in ancestors:
                    #     raise CircularInheritance(node.name)
                
                    # 5b. Check if the superclass is declared
                    # (Uses self.list_class, which was populated in visit_program's Pass 1)
                    if node.name == node.superclass:
                        raise UndeclaredClass(node.superclass)
                    parent_decl = next(
                        filter(lambda c: c.name == current_parent_name, self.list_class), 
                        None
                    )
                
                    if not parent_decl:
                        raise UndeclaredClass(current_parent_name)
                
                    ancestors.add(current_parent_name)
                    current_parent_name = getattr(parent_decl, 'superclass', None) # Assumes 'superclass' attribute
        
        
            # The *starting scope* for the members is an empty class scope
            member_scope_start = []
            member_env = [member_scope_start] + global_env
        
            # 7. Define the lambda for visiting members (Pattern B)
            # 'acc_class_scope' is the class scope being built (starts at [])
            member_lambda = lambda acc_class_scope, member_decl: self.visit(
                member_decl,
                # Pass (scope_being_built, new_full_env_for_members)
                # This rebuilds the env on each loop to fix Undeclared errors:
                # [ [updated_class_scope], [new_global_scope] ]
                (acc_class_scope, member_env) 
            )
        
            # 8. Run reduce to visit all members
            reduce(member_lambda, node.members, member_scope_start)

        finally:
            # 9. Reset the current class context
            self.class_curr = previous_class
        
        # 10. Return the *new* updated global scope for visit_program's reduce
        return global_scope
        
    def find_member(self, class_name: str, member_name: str):
        """
        Helper function to find a member (AttributeDecl or MethodDecl)
        in a class or any of its parent classes.
        """
        current_class_name = class_name
    
        while current_class_name:
            # 1. Find the class declaration
            class_decl = next(
                filter(lambda c: c.name == current_class_name, self.list_class), 
                None
            )
        
            if not class_decl:
                return None # Should not happen if class was declared

            # 2. Search for the member in this class's members
            for mem_decl in class_decl.members:
                if isinstance(mem_decl, AttributeDecl):
                    # 'mem_decl' is (e.g., 'int a, b')
                    for attr in mem_decl.attributes:
                        if attr.name == member_name:
                            return mem_decl # Return the whole AttributeDecl
            
                elif isinstance(mem_decl, (MethodDecl, ConstructorDecl)):
                    if mem_decl.name == member_name:
                        return mem_decl # Return the MethodDecl
        
        # 3. Not found? Move up the inheritance chain
        current_class_name = getattr(class_decl, 'superclass', None) 
        
        # 4. Reached top of the chain, not found
        return None

    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None) -> list[Symbol]:
        """
        Visits an AttributeDecl node (e.g., 'static final int a, b;').
        'o' is a tuple: (current_scope, full_env)
            - o[0] (current_scope): The class_scope being built.
            - o[1] (full_env): The full environment for lookups ([class_scope], [global_scope]).
        """
    
        # 1. Unpack the context
        current_scope = o[0]
        full_env = o[1] 
        try:
            var_type = self.visit(node.attr_type, full_env)
        except UndeclaredClass as e:
            # The visit(node.var_type,...) just raised Undeclared("Class", "B")
            raise e

        # 2. Define the lambda for the inner reduce
        # This lambda will call visit_attribute for each item in 'node.attributes'
        lambda_func = lambda acc_scope, attr_node: self.visit(
            attr_node, 
            # Pack a new, detailed tuple for visit_attribute:
            (
                acc_scope,         # The accumulating class scope
                full_env,          # The full environment for lookups
                node.attr_type,    # The shared type (e.g., 'int')
                node.is_final,     # The shared 'final' flag
                node.is_static     # The shared 'static' flag
            )
        )

        # 3. Run reduce, starting with the current_scope
        # This will add Symbol('a'), then Symbol('b'), etc., to the scope
        try:
            new_scope = reduce(lambda_func, node.attributes, current_scope)
        except TypeMismatchInConstant:
            raise TypeMismatchInConstant(node)
        except TypeMismatchInStatement:
            raise TypeMismatchInStatement(node)

        # 4. Return the updated scope to the outer reduce (in visit_class_decl)
        return new_scope

    def visit_attribute(self, node: "Attribute", o: Any = None) -> list[Symbol]:
        """
        Visits an individual Attribute (e.g., 'a' or 'b = 5').
        'o' is a detailed tuple from visit_attribute_decl:
        (current_scope, full_env, attr_type, is_final, is_static)
        """
    
        # 1. Unpack the detailed tuple
        current_scope, full_env, attr_type, is_final, is_static = o

        # 2. Check for Redeclared in the current class scope
        found = next(filter(lambda sym: sym.name == node.name, current_scope), None)
        if found:
            raise Redeclared("Attribute", node.name)

        # 3. Handle the initializer (if one exists)
        has_init = False
        if node.init_value:
            has_init = True
        
            # 3a. If 'final', expression must be constant
            if is_final:
                if self.check_IllegalConstantExpression(node.init_value, full_env):
                    raise IllegalConstantExpression(str(node.init_value))

            # 3b. Get the type of the initializing expression
            init_type = self.visit(node.init_value, full_env)
        
            # 3c. Check for type compatibility (RHS type must be assignable to LHS type)
            if not self.check_type(attr_type, init_type, can_coerce=True):
                if is_final:
                    raise TypeMismatchInConstant(node)
                raise TypeMismatchInStatement(node) # Or a more specific error
        else:
            if is_final:
                # Biến 'final' mà không có giá trị khởi tạo
                raise IllegalConstantExpression(NilLiteral()) 
    
        # 4. Create the new Symbol for this attribute
        # (This assumes a Symbol constructor like:
        # Symbol(name, type, is_final, is_static, has_init_val))
        new_symbol = Symbol(node.name, attr_type, is_final, is_static, has_init)
                        
        # 5. Return the updated class scope
        return [new_symbol] + current_scope
        
    def visit_method_decl(self, node: "MethodDecl", o: Any= None) -> list[Symbol]:
        # 'o' là môi trường đầy đủ do visit_class_decl truyền vào
        # o[0] là class_scope
        class_scope = o[0]
        full_env = o[1]
    
        # 1. Kiểm tra Redeclared Method trong class_scope
        found = next(filter(lambda sym: sym.name == node.name, class_scope), None)
        if found:
            raise Redeclared("Method", node.name)

        # 2. Quản lý trạng thái method_curr
        previous_method = self.method_curr
        self.method_curr = node
    
        try:
            # 3. Tạo Phạm vi Tham số (Scope o[-3] ban đầu)
            if node.params is not None:
                param_lambda = lambda acc, param_decl: self.visit(
                    param_decl,
                    (acc, full_env) # Dùng 'member_env' để tra cứu (nếu cần)
                )
                populated_param_scope = reduce(param_lambda, node.params, [])
            else:
                populated_param_scope = []
    
            # 4. Tạo Môi trường Đầy đủ cho Thân hàm
            # [ [param_scope], [class_scope], [global_scope] ]
            body_lambda = lambda acc_scope, stmt: self.visit(
                stmt,
                # Xây dựng lại full_env MỚI mỗi lần: [acc_scope] + member_env
                (acc_scope, [acc_scope] + full_env) 
            )
            #body_environment = [populated_param_scope] + full_env
            var_decl_scope = reduce(body_lambda, node.body.var_decls, populated_param_scope)
            stmt_lambda = lambda acc_scope, stmt: self.visit(
                stmt,
                # Rebuild env so 'y := x + 1' can find 'x'
                (acc_scope, [acc_scope] + full_env) 
            )
        
            # Start reduce *with* the scope from Phase 2
            reduce(stmt_lambda, node.body.statements, var_decl_scope)
        
        finally:
            self.method_curr = previous_method
    
        # 7. Trả về class_scope đã cập nhật (cho reduce của visit_class_decl)
        param_types = [param.param_type for param in node.params]
        return_type = node.return_type
    
        # (Logic tạo Symbol của bạn)
        if node.is_static:
            new_sym = Symbol(node.name, FunctionType(param_types, return_type), False, True, False)
        else:
            new_sym = Symbol(node.name, FunctionType(param_types, return_type), False, False, False)
        
        return [new_sym] + class_scope

    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None) -> list[Symbol]:
        """
        Visits a ConstructorDecl node.
        'o' is a tuple: (class_scope, full_env)
        Returns the updated class_scope.
        """
    
        # 1. Unpack the context
        # 'o' is a tuple: (class_scope, full_env)
        class_scope = o[0]
        full_env = o[1] # full_env is [[class_scope], [global_scope]]

        # 2. Check for Redeclared Constructor

        # 3. Manage the current method state
        previous_method = self.method_curr
        self.method_curr = node

        try:
            # 4. Create the parameter scope
            # FIX: Pass the full_env (o[1]) to the parameter's visit function,
            # not the whole tuple 'o'.
            param_lambda = lambda acc, param_decl: self.visit(
                param_decl,
                (acc, full_env) # Pass (accumulating_scope, full_env)
            )
        
            populated_param_scope = reduce(param_lambda, node.params, [])

            # 5. Create the environment for the constructor's body
            # FIX: Use full_env (o[1]) to build the new env, not the tuple 'o'
            # This creates: [[local_scope], [param_scope], [class_scope], [global_scope]]
            body_environment = [[]] + [populated_param_scope] + full_env
    
            # 6. Visit the body
            self.visit(node.body, body_environment)

        finally:
            # 7. FIX: Use 'finally' to guarantee state restoration
            # even if self.visit(node.body,...) raises an error.
            self.method_curr = previous_method

        # 8. Return the updated class_scope
        param_types = [param.param_type for param in node.params]
        new_symbol = Symbol(node.name, FunctionType(param_types, PrimitiveType("void")), False, False, False, method_type="constructor")
    
        return [new_symbol] + class_scope
        

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None) -> list[Symbol]:
        """
        Visits a DestructorDecl node.
        'o' is a tuple: (class_scope, full_env)
        Returns the updated class_scope.
        """

        # 1. Unpack the context
        class_scope = o[0]
        full_env = o[1]

        # # 2. Check for Redeclared Destructor
        found = next(filter(lambda sym: sym.name == node.name, class_scope), None)
        if found and found.method_type == "destructor":
            raise Redeclared("Destructor", node.name)

        # 3. Manage the current method state
        previous_method = self.method_curr
        self.method_curr = node

        try:
            # 4. Create the parameter scope
            # FIX: The DestructorDecl node has NO 'params' attribute.
            # The parameter scope is always empty.
            populated_param_scope = [] 
        
            # 5. Create the environment for the constructor's body
            # FIX: Use full_env (o[1]), not the tuple 'o'
            body_environment = [[]] + [populated_param_scope] + full_env
    
            # 6. Visit the body
            self.visit(node.body, body_environment)

        finally:
            # 7. FIX: Use 'finally'
            self.method_curr = previous_method

        # 8. Return the updated class_scope
        # FIX: FunctionType should have no parameters
        new_symbol = Symbol(node.name, FunctionType([], PrimitiveType("void")), False, False, False, method_type="destructor")
    
        return [new_symbol] + class_scope

    def visit_parameter(self, node: "Parameter", o: Any = None) -> list[Symbol]:
        """
        Duyệt một nút Parameter (tham số).
        'o' là một tuple: (acc_scope, full_env)
            - o[0] (acc_scope): Phạm vi tham số đang được xây dựng (acc của reduce).
            - o[1] (full_env): Môi trường đầy đủ (vd: [[class_scope], [global_scope]]).
        """
    
        # 1. Lấy phạm vi tham số đang được xây dựng (từ o[0])
        current_param_scope = o[0]
        if isinstance(node.param_type, ClassType):
            self.visit(node.param_type, o[1])
    
        # 2. Kiểm tra Redeclared (logic này đã có trong stub của bạn)
        found = next(filter(lambda sym: sym.name == node.name, current_param_scope), None)
        if found:
            # Nếu tìm thấy, ném lỗi
            raise Redeclared("Parameter", node.name)
    
        # 3. Tạo Symbol mới cho tham số
        # (Giả định tham số không bao giờ là 'final')
        new_symbol = Symbol(node.name, node.param_type, isFinal=False) 
    
        # 4. Trả về scope tham số đã cập nhật
        # (thêm symbol mới vào đầu danh sách)
        return [new_symbol] + current_param_scope

    def visit_block_statement(self, node: "BlockStatement", o: Any = None) -> list[Symbol]:
        """
        Duyệt một nút BlockStatement (KHỐI LỒNG NHAU).
        Hàm này tạo ra một phạm vi lồng nhau mới.
    
        'o' là một tuple: (parent_scope, parent_full_env)
            - o[0] (parent_scope): Phạm vi của cha (vd: [y, z]).
            - o[1] (parent_full_env): Môi trường đầy đủ của cha (vd: [[y, z], [class], [global]]).
        """
    
        # 1. Giải nén ngữ cảnh (context) của cha
        parent_scope = o[0]
        parent_full_env = o[1]

        # 2. TẠO MỘT MÔI TRƯỜNG LỒNG NHAU MỚI
        #    Tạo một scope rỗng [[]] cho các biến cục bộ (vd: 'k')
        #    và đặt nó lên trước môi trường của cha.
        #   vd: [ [], [y, z], [class], [global] ]
        nested_full_env = [[]] + parent_full_env
    
        # === GIAI ĐOẠN 1: Xử lý Khai báo Biến (var_decls) ===
    
        # 'acc_scope' là scope lồng nhau (nested_full_env[0]) đang được xây dựng
        lambda_vars = lambda acc_scope, var_decl_stmt: self.visit(
            var_decl_stmt,
            (acc_scope, [acc_scope] + nested_full_env) # Truyền (scope 'k', env lồng nhau)
        )

        # Chạy reduce, bắt đầu với scope rỗng (nested_full_env[0])
        # 'scope_after_vars' sẽ là scope lồng nhau đã được điền (vd: [Symbol('k')])
        scope_after_vars = reduce(lambda_vars, node.var_decls, nested_full_env[0])

        # === GIAI ĐOẠN 2: Xử lý Câu lệnh (statements) ===

        # Môi trường đầy đủ cho các câu lệnh con PHẢI bao gồm các biến vừa khai báo
        # vd: [ [Symbol('k')], [y, z], [class], [global] ]
        stmts_full_env = [scope_after_vars] + parent_full_env
    
        # 'acc_scope' là 'scope_after_vars' (vd: [Symbol('k')])
        lambda_stmts = lambda acc_scope, stmt: self.visit(
            stmt,
            # Truyền (scope 'k', env lồng nhau ĐÃ CẬP NHẬT)
            (acc_scope, stmts_full_env)
        )

        # Chạy reduce trên các câu lệnh con (if, for, assign, ...)
        # Bắt đầu với 'scope_after_vars'
        reduce(lambda_stmts, node.statements, scope_after_vars)

        # 5. Trả về
        #    'reduce' của hàm cha (đã gọi 'visit_block_statement')
        #    cần nhận lại 'parent_scope' (o[0]) không thay đổi.
        #    Biến 'k' không thuộc về scope [y, z].
    
        return parent_scope
    
    def check_IllegalConstantExpression(self, node: Expr, o: list[list[Symbol]]) -> bool:
        if isinstance(node, Literal) and not isinstance(node, NilLiteral):
            return False
        if isinstance(node, NilLiteral):
            return True
        if isinstance(node, Identifier):
            # TODO
            found_symbol = None
            for scope in o:  # Tìm trong tất cả các scope
                found_symbol = next(filter(lambda sym: sym.name == node.name, scope), None)
                if found_symbol:
                    break
        
            # Phải tìm thấy và phải là 'final'
            # (Giả sử Symbol có 'is_final' hoặc 'kind' là Constant)
            if found_symbol and hasattr(found_symbol, 'isFinal') and found_symbol.isFinal:
                return False  # Hợp lệ
            else:
                return True  # Không hợp lệ (không tìm thấy hoặc không phải final)
        if isinstance(node, BinaryOp):
            # TODO
            return self.check_IllegalConstantExpression(node.left, o) or self.check_IllegalConstantExpression(node.right, o)
        if isinstance(node, UnaryOp):
            return self.check_IllegalConstantExpression(node.operand, o)
        if isinstance(node, ParenthesizedExpression):
            return False
        if isinstance(node, ThisExpression):
            # 'this' by itself is a valid base for a constant expression
            # (e.g., this.MAX_SIZE). We must treat it as Legal.
            return False
        if isinstance(node, PostfixExpression):
            try:
                primary = node.primary
                current_type = None
                check_static = False # Flag để kiểm tra truy cập tĩnh

                # 1. Xử lý phần gốc (primary) của biểu thức
            
                if isinstance(primary, ThisExpression):
                    # Trường hợp: 'this.MAX_SIZE'
                    # 'this' là hợp lệ trong một biểu thức hằng số
                    # (miễn là nó không ở trong phương thức static,
                    # nhưng visit_this_expression sẽ xử lý việc đó)
                    current_type = self.visit(primary, o)
                    check_static = False # 'this' luôn là truy cập instance

                elif isinstance(primary, Identifier):
                    # Trường hợp: 'MyClass.STATIC_FIELD' hoặc 'OTHER_CONST.FIELD'
                
                    # Kiểm tra xem 'Identifier' gốc có phải là hằng số không
                    if self.check_IllegalConstantExpression(primary, o):
                        return True # Không hợp lệ (gốc không phải hằng số)
                
                    current_type = self.visit(primary, o)
                    # Kiểm tra xem đây có phải là truy cập tĩnh không
                    check_static = any(c.name == primary.name for c in self.list_class)

                else:
                    # Bất kỳ gốc nào khác (vd: 'new A()', '1', 'a+b')
                    # đều không hợp lệ
                    return True # Không hợp lệ

                # 2. Duyệt qua chuỗi truy cập (postfix_ops)
                for item in node.postfix_ops:
                    if isinstance(item, MemberAccess):
                        member_name = item.member_name
                
                        if not isinstance(current_type, ClassType):
                            return True # Lỗi: truy cập '.member' trên kiểu không phải Class

                        # Tìm ClassDecl
                        class_name = current_type.class_name
                        class_decl_node = next(filter(lambda c: c.name == class_name, self.list_class), None)

                        if not class_decl_node:
                            return True # Không tìm thấy định nghĩa Class

                        # Tìm thành viên (member) trong lớp
                        found_member = False
                        member_decl = None # Giữ 'AttributeDecl'
                    
                        for mem_decl in class_decl_node.members:
                            if isinstance(mem_decl, AttributeDecl):
                                
                                # --- ĐÂY LÀ PHẦN SỬA LỖI ---
                                # Sử dụng 'isFinal' (camelCase)
                                if not mem_decl.is_final:
                                    continue # Bỏ qua nếu không phải 'final'
                                # --- KẾT THÚC SỬA LỖI ---

                                # Duyệt các thuộc tính trong khai báo (vd: final int a, b)
                                for attr in mem_decl.attributes:
                                    if attr.name == member_name:
                                        current_type = mem_decl.attr_type
                                        member_decl = mem_decl
                                        found_member = True
                                        break
                            if found_member:
                                break
                    
                        if not found_member:
                            # Không tìm thấy, HOẶC tìm thấy nhưng không 'final'
                            return True # Không hợp lệ
                    
                        # Kiểm tra truy cập static/instance
                        if check_static and not member_decl.is_static:
                            return True # Lỗi: MyClass.instance_field
                        if not check_static and member_decl.is_static:
                            return True # Lỗi: my_instance.static_field

                    else: 
                        # Bất kỳ thao tác nào khác (FuncCall '()', ArrayAccess '[]')
                        # đều không hợp lệ trong một hằng số
                        return True # Không hợp lệ

            # Nếu vòng lặp kết thúc mà không 'return True',
            # có nghĩa là toàn bộ chuỗi hợp lệ
                return False # Hợp lệ

            except Exception:
                # Bất kỳ lỗi nào (Undeclared, ...) đều có nghĩa là không hợp lệ
                return True
        return False
    
    def check_type(self, left: Type, right: Type, can_coerce: bool = True) -> bool:
        if isinstance(right, ClassType) and isinstance(left, ClassType) and right.class_name == "":
            return True
        if isinstance(left, ReferenceType):
            ## TODO
            return self.check_type(left.referenced_type, right, can_coerce)
        if isinstance(right, ReferenceType):
            ## TODO
            return self.check_type(left, right.referenced_type, can_coerce)
        if isinstance(left, PrimitiveType) and isinstance(right, PrimitiveType):
            ## TODO
            if left.type_name == right.type_name:
                return True
            if can_coerce:
            # This will fix test_071
                if left.type_name == "float" and right.type_name == "int":
                    return True
            return False
        if isinstance(left, ArrayType) and isinstance(right, ArrayType):
            ## TODO
            left_to_right = self.check_type(right.element_type, left.element_type, can_coerce=False)
            right_to_left = self.check_type(left.element_type, right.element_type, can_coerce=False)
        
            return left_to_right and right_to_left
        if isinstance(left, ClassType) and isinstance(right, ClassType):
            ## TODO
            # 4a. Nếu hai lớp giống hệt nhau
            if left.class_name == right.class_name:
                return True
            
            # 4b. Kiểm tra tính kế thừa: 'right' (con) có thể gán cho 'left' (cha)
            # (Giả định 'self.list_class' đã được điền từ visit_program)
        
            current_class_name = right.class_name
            while current_class_name:
                # Tìm ClassDecl của lớp hiện tại
                class_decl = next(
                    filter(lambda c: c.name == current_class_name, self.list_class), 
                    None
                )
            
                if not class_decl:
                    # Không tìm thấy định nghĩa lớp
                    return False
                
                # Giả sử ClassDecl có thuộc tính 'parent_name' (kiểu str)
                parent_name = getattr(class_decl, 'superclass', None)
            
                if parent_name == left.class_name:
                    # Tìm thấy! 'right' là con của 'left'
                    return True
                
                # Di chuyển lên cây kế thừa
                current_class_name = parent_name
            
            # Đã duyệt hết cây mà không tìm thấy -> không phải cha con
            return False
        return False
        
    def visit_variable_decl(self, node: "VariableDecl", o: Any = None) -> list[Symbol]:
        # 'o' là môi trường đầy đủ [ [local_scope], [param_scope], ... ]
        # 1. Giải nén tham số đầu vào
        current_scope = o[0]
        full_env = o[1]

        try:
            var_type = self.visit(node.var_type, full_env)
        except UndeclaredClass as e:
            # The visit(node.var_type,...) just raised Undeclared("Class", "B")
            raise e

        lambda_func = lambda acc, var_node: self.visit(
            var_node, 
            (acc, full_env, node.var_type, node.is_final)
        )
        try:
            new_scope = reduce(lambda_func, node.variables, current_scope)
        except TypeMismatchInStatement:
            raise TypeMismatchInStatement(node)
        except TypeMismatchInConstant:
            raise TypeMismatchInConstant(node)
        # 4. Trả về phạm vi MỚI đã cập nhật
        return new_scope


    def visit_variable(self, node: "Variable", o: Any = None): 
        # 1. Giải nén tuple tham số
        current_scope, full_env, var_type, is_final = o
        is_assign = False

        
    
        # 2. Kiểm tra Redeclared (MẤU CHỐT CỦA TEST 002)
        #    Chỉ kiểm tra trong phạm vi hiện tại (current_scope, o[0]).
        found = next(filter(lambda sym: sym.name == node.name, current_scope), None)
        if found:
            # Lần 1: current_scope = [], found = None -> OK
            # Lần 2: current_scope = [Symbol('x')], found = Symbol('x') -> LỖI
            if is_final:
                raise Redeclared("Constant", node.name)
            raise Redeclared("Variable", node.name)
        
        # 3. Xử lý giá trị khởi tạo (nếu có)
        if node.init_value:
            # 3a. Kiểm tra 'final' (hằng số)
            is_assign = True
            if is_final:
                # Dùng 'full_env' (o[1]) để tra cứu hằng số khác (nếu có)
                is_illegal = self.check_IllegalConstantExpression(node.init_value, full_env)
                if is_illegal:
                    raise IllegalConstantExpression(str(node.init_value))
                
            # 3b. Kiểm tra kiểu
            # Dùng 'full_env' (o[1]) để visit biểu thức vế phải
            right_type = self.visit(node.init_value, full_env)

            # 3c. So sánh kiểu
            if not self.check_type(var_type, right_type, can_coerce=True):
                if is_final:
                    raise TypeMismatchInConstant(node)
                raise TypeMismatchInStatement(node) # Check Type Mismatch
        else:
            if is_final:
                # Biến 'final' mà không có giá trị khởi tạo
                raise IllegalConstantExpression(NilLiteral())
            
        # 4. Tạo Symbol mới
        # (Giả sử Symbol của bạn chấp nhận isFinal)
        new_symbol = Symbol(node.name, var_type, isFinal=is_final, isAssigned=is_assign)
    
        # 5. Trả về phạm vi hiện tại đã được cập nhật
        # (vd: [Symbol('x')] + [])
        # current_scope.append(new_symbol)
        return [new_symbol] + current_scope

    def visit_assignment_statement(self, node: "AssignmentStatement", o: Any = None) -> list[Symbol]:
        ## TODO
        # 1. Giải nén môi trường
        current_scope = o[0]
        full_env = o[1]  # Dùng full_env để tra cứu và kiểm tra kiểu
        #lhs_type,found = self.visit(node.lhs, full_env)
        lhs_node = node.lhs


        # Trường hợp 1: LHS là identifier
        try:
            self.visit(lhs_node, full_env)
        except CannotAssignToConstant:
            raise CannotAssignToConstant(node)
        
        # Lấy kiểu để so sánh
        
        typ_rhs = self.visit(node.rhs, full_env)
        typ_lhs,_ = self.visit(node.lhs, full_env)
        ## TODO TypeMismatchInStatement
        if not self.check_type(typ_lhs, typ_rhs, can_coerce=True):
            raise TypeMismatchInStatement(node)
        if isinstance(node.rhs, ArrayLiteral) or isinstance(typ_rhs, ArrayType):
            if typ_lhs.size != typ_rhs.size:
                raise TypeMismatchInStatement(node)
        return current_scope

    def visit_for_statement(self, node: "ForStatement", o: Any = None) -> list[Symbol]:
        typ: Type

        ## TODO 
        current_scope = o[0]
        full_env = o[1]

        typ_start = self.visit(node.start_expr, full_env)

        if not self.check_type(typ_start, PrimitiveType("int"), False):
            raise TypeMismatchInStatement(node)
        
        typ_end = self.visit(node.end_expr, full_env)

        if not self.check_type(typ_end, PrimitiveType("int"), False):
            raise TypeMismatchInStatement(node)

        ## TODO TypeMismatchInStatement

        # 4. Xử lý biến lặp (PHẦN ĐƯỢC CẬP NHẬT)
    
        body_env = None  # Môi trường sẽ dùng để visit thân vòng lặp
        found_sym = next(filter(lambda sym: sym.name == node.variable, current_scope), None)

        if found_sym:
            # TRƯỜNG HỢP 1: Biến đã tồn tại
        
            # 4a. Kiểm tra kiểu
            if not self.check_type(found_sym.typ, PrimitiveType("int"), False):
                # Tồn tại nhưng sai kiểu
                raise TypeMismatchInStatement(node)
            
            # 4b. Kiểm tra 'final'
            if found_sym.isFinal:
                # Tồn tại, đúng kiểu, nhưng là 'final'
                # (Vòng lặp 'for' cần gán lại giá trị, nên đây là lỗi)
                raise CannotAssignToConstant(node)
            
            # 4c. Hợp lệ. Thân vòng lặp sẽ dùng lại 'full_env'
            # Chúng ta chỉ thêm một scope rỗng [[]] cho các biến cục bộ CỦA body
            body_env = [[]] + full_env

        else:
            # TRƯỜNG HỢP 2: Biến chưa tồn tại
        
            # Tạo Symbol mới cho nó
            # (Biến lặp 'for' thường được coi là 'final' BÊN TRONG thân vòng lặp)
            loop_var_sym = Symbol(node.variable, PrimitiveType("int"), isFinal=True)
            loop_var_scope = [loop_var_sym]
        
            # Tạo môi trường mới cho body
            body_env = [[]] + [loop_var_scope] + full_env
    
            self.loop += 1
            self.visit(node.body, o)
            self.loop -= 1
            return o[0]
        # 5. Duyệt thân vòng lặp
        self.loop += 1
        self.visit(node.body, (body_env[0], body_env)) # Dùng 'body_env' đã được quyết định
        self.loop -= 1

        # 6. Trả về scope
        # 'current_scope' (o[0]) của hàm cha không thay đổi
        return current_scope

    def visit_break_statement(self, node: "BreakStatement", o: Any = None) -> list[Symbol]:
        ## TODO
        current_scope = o[0]
        if self.loop == 0:
            raise MustInLoop(node)
        
        return current_scope


    def visit_continue_statement(self, node: "ContinueStatement", o: Any = None) -> list[Symbol]:
        ## TODO
        current_scope = o[0]
        if self.loop == 0:
            raise MustInLoop(node)
        
        return current_scope

    def visit_id_lhs(self, node: "IdLHS", o: list[list[Symbol]] = None) -> Tuple[Type, Symbol]:
        found = None
        found_in_scope_index = -1
        for i, scope in enumerate(o):
            found = next(filter(lambda sym: sym.name == node.name, scope), None)
            if found:
                found_in_scope_index = i
                break
        if not found:
            raise UndeclaredIdentifier(node.name)
        if found.isFinal:
            raise CannotAssignToConstant(node)
        
        is_static_context = self.method_curr and self.method_curr.is_static
    
        # 2. Check if the found symbol is an instance member
        # (i.e., it's a class member and 'is_static' is False)
        is_instance_member = (not found.isStatic) 

        size_symbol = len(o)

        if size_symbol == 4:
            is_member = (found_in_scope_index >= 2)
        elif size_symbol ==3:
            is_member = (found_in_scope_index >=1)
    
        # 3. If both are true, it's an illegal access.
        if is_static_context and is_instance_member and is_member:
        # This is the illegal access from test_038.
            raise UndeclaredIdentifier(node.name)
        return (found.typ, found)
    
    def visit_postfix_lhs(self, node: "PostfixLHS", o: list[list[Symbol]] = None) -> Tuple[Type, AttributeDecl]:
        Node = node.postfix_expr
        obj: ClassType | ArrayType | None = None
        check_static: bool = False
        if isinstance(Node.primary, Identifier):
            ## TODO
            primary_name = Node.primary.name
            found_sym = None
            for scope in o:
                found_sym = next(filter(lambda sym: sym.name == Node.primary.name, scope), None)
                if found_sym:
                    break

            if not found_sym:
                raise UndeclaredIdentifier(Node.primary.name)
            
            is_class_name = any(c.name == primary_name for c in self.list_class)

            if is_class_name and isinstance(found_sym.typ, ClassType):
                check_static = True
                obj = found_sym.typ
            else:
                check_static = False
                obj = found_sym.typ
        else:  
            obj = self.visit(Node.primary, o)
            check_static = False

        member: AttributeDecl | None = None
        for item in Node.postfix_ops:
            if isinstance(item, MemberAccess):

                if not isinstance(obj, ClassType):
                    raise TypeMismatchInExpression(node.postfix_expr)
              
                current_class = next((c for c in self.list_class if c.name == obj.class_name), None)
                if not current_class:
                    raise UndeclaredClass(obj.class_name)
              
                member = None # member ở đây là AttributeDecl
                found_in_loop = False
                # ## TODO: (ĐÂY LÀ LOGIC ĐÃ SỬA)
                # Duyệt qua các thành viên (AttributeDecl, MethodDecl,...) của lớp
                for mem_decl in current_class.members:
                    # Chỉ quan tâm AttributeDecl
                    if isinstance(mem_decl, AttributeDecl):
                        # 'mem_decl' là (static final int a, b)
                        # Giờ kiểm tra xem 'item.member_name' (ví dụ 'a') 
                        # có nằm trong danh sách 'mem_decl.attributes' không
                        for attr_node in mem_decl.attributes:
                            if attr_node.name == item.member_name:
                                # Tìm thấy! 'member' chính là 'mem_decl' (toàn bộ dòng)
                                member = mem_decl 
                                found_in_loop = True
                                break
                    if found_in_loop:
                        # if member.is_final:
                        #     raise CannotAssignToConstant(node)
                        break

                if not member:
                    if current_class.superclass:
                        # Tìm trong lớp cha
                        parent_class = next((c for c in self.list_class if c.name == current_class.superclass), None)
                        while parent_class:
                            for mem_decl in parent_class.members:
                                if isinstance(mem_decl, AttributeDecl):
                                    for attr_node in mem_decl.attributes:
                                        if attr_node.name == item.member_name:
                                            member = mem_decl
                                            found_in_loop = True
                                            break
                                if found_in_loop:
                                    # if member.is_final:
                                    #     raise CannotAssignToConstant(node)
                                    break
                            if member:
                                break
                            if parent_class.superclass:
                                parent_class = next((c for c in self.list_class if c.name == parent_class.superclass), None)
                            else:
                                parent_class = None
                    else:
                        raise UndeclaredAttribute(item.member_name)

                #member_decl = self.find_member(obj.class_name, item.member_name)
                # --- END FIX ---

                if not member:
                    raise UndeclaredAttribute(item.member_name) # Correctly finds 'c' now
                    
                # (Your checks for static access would go here)

                #current_type = member_decl.attr_type
              
                # if member_decl and member_decl.is_final :
                #     raise CannotAssignToConstant(node)           
              
                # 'member' là AttributeDecl, nên nó có .is_static
                if check_static and not member.is_static:
                    raise IllegalMemberAccess(f".{item.member_name}")
                if not check_static and member.is_static:
                    raise IllegalMemberAccess(f".{item.member_name}")
              
                # 'member' là AttributeDecl, nên nó có .attr_type
                obj = member.attr_type

            elif isinstance(item, ArrayAccess):
                # Thao tác là truy cập mảng (vd: [i])
            
                # ## TODO: Xử lý ArrayAccess
            
                # 1. Kiểm tra 'obj' có phải là ArrayType không
                if not isinstance(obj, ArrayType):
                    raise TypeMismatchInExpression(node.postfix_expr)
                
                # 2. Kiểm tra kiểu của biểu thức index (phải là int)
                index_type = self.visit(item.index, o)
                if not self.check_type(index_type, PrimitiveType("int"), False):
                    raise TypeMismatchInExpression(node.postfix_expr)
            
                # 3. Cập nhật 'obj' thành kiểu của phần tử mảng
                obj = obj.element_type
            
                # 4. QUAN TRỌNG:
                # Vì thao tác cuối là [i], chúng ta không trả về AttributeDecl.
                # Điều này cho phép 'a.b[i] := 1' ngay cả khi 'b' là 'final'.
                member = None

        if member and member.is_final:
            raise CannotAssignToConstant(node)

        return obj, member
    

    def visit_identifier(self, node: "Identifier", o: list[list[Symbol]] = None) -> Type:
        found = None
        found_in_scope_index = -1
        for i, scope in enumerate(o):
            found = next(filter(lambda sym: sym.name == node.name, scope), None)
            if found:
                found_in_scope_index = i
                break

        if not found:
            raise UndeclaredIdentifier(node.name) 
        # if not found.isAssigned:
        #     raise UndeclaredIdentifier(node.name)
        is_static_context = self.method_curr and self.method_curr.is_static
    
        # 2. Check if the found symbol is an instance member
        # (i.e., it's a class member and 'is_static' is False)
        is_class_member = (found_in_scope_index == 2)
    
        # 3. If both are true, it's an illegal access.
        if is_class_member:
        # 3. If it's a class member, check its 'is_static' flag
            is_instance_member = not found.isStatic
            if is_static_context and is_instance_member:
                # This is the 'test_038' error (static access to instance field)
                raise UndeclaredIdentifier(node.name)
        return found.typ

    def _get_postfix_info(self, node: "PostfixExpression", o: list[list[Symbol]] = None) -> Tuple[Type, bool]:
        obj: Type | None = None
        check_static: bool = False
        if isinstance(node.primary, Identifier):
            ## TODO
            found_sym = None
            for scope in o:
                found_sym = next(filter(lambda sym: sym.name == node.primary.name, scope), None)
                if found_sym:
                    break

            if not found_sym:
                raise UndeclaredIdentifier(node.primary.name)
            is_class_name = any(c.name == node.primary.name for c in self.list_class)
            if is_class_name and isinstance(found_sym.typ, ClassType):
                # Đây là truy cập tĩnh (vd: 'MyClass'.static_field)
                check_static = True
            else:
                # Đây là truy cập instance (vd: 'my_obj'.field)
                check_static = False
            obj = found_sym.typ
        else:  
            obj = self.visit(node.primary, o)
            check_static = False


        for item in node.postfix_ops:
            if isinstance(item, MemberAccess):
                ## TODO
                # if not isinstance(item, ClassType):
                #     raise TypeMismatchInExpression(node)
                if not isinstance(obj, ClassType):
                    raise TypeMismatchInExpression(node)
                
                member_name = item.member_name
                current_class_name = obj.class_name
                member_decl = None
                while current_class_name:
                    # 1. Find the class declaration
                    class_decl = next(
                        filter(lambda c: c.name == current_class_name, self.list_class), None)
    
                    if not class_decl:
                    # This shouldn't happen if UndeclaredClass check is working
                        break 

                    # 2. Search for the member in *this* class's members
                    found_in_this_class = False
                    for mem_decl in class_decl.members:
                        if isinstance(mem_decl, AttributeDecl):
                            for attr in mem_decl.attributes:
                                if attr.name == member_name:
                                    member_decl = mem_decl # Found it!
                                    found_in_this_class = True
                                    break
                        elif isinstance(mem_decl, (MethodDecl, ConstructorDecl)):
                            if mem_decl.name == member_name:
                                member_decl = mem_decl # Found it!
                                found_in_this_class = True
                                break
                        
                        if found_in_this_class:
                            break
                    
                    if found_in_this_class:
                        break # Stop the outer 'while' loop

                    # 3. Not found? Move up the inheritance tree
                    current_class_name = getattr(class_decl, 'superclass', None)
                
                if not member_decl:
                    raise UndeclaredAttribute(item.member_name)
                
                # Kiểm tra truy cập static/instance
                if check_static and not member_decl.is_static:
                    raise IllegalMemberAccess(f".{item.member_name}") # Lỗi: MyClass.instance_field
                if not check_static and member_decl.is_static:
                    raise IllegalMemberAccess(f".{item.member_name}") # Lỗi: my_obj.static_field

                # Cập nhật 'obj' thành kiểu của thuộc tính
                obj = member_decl.attr_type
                check_static = False # Sau lần truy cập đầu tiên, luôn là instance

            elif isinstance(item, MethodCall):
                ## TODO               
                if not isinstance(obj, ClassType):
                    raise TypeMismatchInExpression(node)
                current_class = next((c for c in self.list_class if c.name == obj.class_name), None)
                if not current_class:
                    raise UndeclaredClass(obj.class_name)
                
                # Tìm phương thức trong các thành viên của lớp
                found_method_decl = None
                for mem_decl in current_class.members:
                    if isinstance(mem_decl, MethodDecl) and mem_decl.name == item.method_name: # Giả sử 'item.name'
                        found_method_decl = mem_decl
                        break
                
                if not found_method_decl:
                    if current_class.superclass:
                        # Tìm trong lớp cha
                        parent_class = next((c for c in self.list_class if c.name == current_class.superclass), None)
                        while parent_class:
                            for mem_decl in parent_class.members:
                                if isinstance(mem_decl, MethodDecl) and mem_decl.name == item.method_name:
                                    found_method_decl = mem_decl
                                    break
                            if found_method_decl:
                                break
                            if parent_class.superclass:
                                parent_class = next((c for c in self.list_class if c.name == parent_class.superclass), None)
                            else:
                                parent_class = None
                if not found_method_decl:
                    raise UndeclaredMethod(item.method_name)
                # Kiểm tra truy cập static/instance
                if check_static and not found_method_decl.is_static:
                    raise IllegalMemberAccess(f".{item.method_name}()")
                if not check_static and found_method_decl.is_static:
                    raise IllegalMemberAccess(f"{item.__str__()}")
                
                # Kiểm tra kiểu của đối số (arguments)
                arg_types = [self.visit(arg, o) for arg in item.args] # Giả sử 'item.args'
                param_types = [p.param_type for p in found_method_decl.params]

                if len(arg_types) != len(param_types):
                    raise TypeMismatchInExpression(node)
                
                for (left_param, right_arg) in zip(param_types, arg_types):
                    if not self.check_type(left_param, right_arg, can_coerce=True):
                        raise TypeMismatchInExpression(node)
                if isinstance(found_method_decl.return_type, PrimitiveType) and found_method_decl.return_type.type_name == 'void':
                    raise TypeMismatchInExpression(node)
                    
                # Cập nhật 'obj' thành kiểu TRẢ VỀ của phương thức
                obj = found_method_decl.return_type
                check_static = False

            elif isinstance(item, ArrayAccess):
                ## TODO
                if not isinstance(obj, ArrayType):
                    raise TypeMismatchInExpression(node)
                
                # Kiểm tra kiểu của index (phải là int)
                index_type = self.visit(item.index, o) # Giả sử 'item.index_expr'
                if not self.check_type(index_type, PrimitiveType("int"), can_coerce=False):
                    raise TypeMismatchInExpression(node)
                
                # Cập nhật 'obj' thành kiểu PHẦN TỬ của mảng
                obj = obj.element_type
                check_static = False


        return obj, check_static
    
    def visit_postfix_expression(self, node: "PostfixExpression", o: list[list[Symbol]] = None) -> Type:
        # Gọi helper
        obj_type, _ = self._get_postfix_info(node, o)
        # Chỉ trả về Type, giữ nguyên "giao diện" cho các hàm khác
        return obj_type

    def visit_method_invocation_statement(self, node: "MethodInvocationStatement", o: Any = None) -> list[Symbol]:
        (typ, check_static) = self._get_postfix_info(PostfixExpression(node.method_call.primary, node.method_call.postfix_ops[:-1]), o[1])
        method_call_op = node.method_call.postfix_ops[-1]
        if not isinstance(typ, ClassType):
            raise TypeMismatchInStatement(node)
        current_class = next((c for c in self.list_class if c.name == typ.class_name), None)
        if not current_class:
            raise UndeclaredClass(typ.class_name)

        # Tìm phương thức
        found_method_decl = None
        for mem_decl in current_class.members:
            # Giả sử MethodDecl và ConstructorDecl có 'name' và 'params'
            if isinstance(mem_decl, MethodDecl) and mem_decl.name == method_call_op.method_name:
                found_method_decl = mem_decl
                break
        
        if not found_method_decl:
            if current_class.superclass:
                # Tìm trong lớp cha
                parent_class = next((c for c in self.list_class if c.name == current_class.superclass), None)
                while parent_class:
                    for mem_decl in parent_class.members:
                        if isinstance(mem_decl, MethodDecl) and mem_decl.name == method_call_op.method_name:
                            found_method_decl = mem_decl
                            break
                    if found_method_decl:
                        break
                    if parent_class.superclass:
                        parent_class = next((c for c in self.list_class if c.name == parent_class.superclass), None)
                    else:
                        parent_class = None
            
        if not found_method_decl:
            raise UndeclaredMethod(method_call_op.method_name)
        
        # Kiểm tra static/instance
        if check_static and not found_method_decl.is_static:
            raise IllegalMemberAccess(node.method_call.postfix_ops[-1])
        if not check_static and found_method_decl.is_static:
            raise IllegalMemberAccess(node.method_call.postfix_ops[-1])

        # Kiểm tra kiểu của đối số
        arg_types = [self.visit(arg, o[1]) for arg in method_call_op.args]
        param_types = [p.param_type for p in found_method_decl.params]

        if len(arg_types) != len(param_types):
            raise TypeMismatchInStatement(node)

        for (left_param, right_arg) in zip(param_types, arg_types):
            if not self.check_type(left_param, right_arg, can_coerce=True):
                raise TypeMismatchInStatement(node)
        # if isinstance(found_method_decl.return_type, PrimitiveType):
        #     if not found_method_decl.return_type.type_name == 'void':
        #         raise TypeMismatchInStatement(node)

        return o[0]

    
    def visit_this_expression(self, node: "ThisExpression", o: list[list[Symbol]] = None) -> ClassType:
        if self.method_curr and isinstance(self.method_curr, MethodDecl):
            if self.method_curr.is_static:
                raise IllegalMemberAccess(node)
        return ClassType(self.class_curr.name)

    
    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None) -> Type:
        if not node.value:
            raise IllegalArrayLiteral(node)
        type_ele = self.visit(node.value[0], o)
        for item in node.value:
            ## TODO
            item_type = self.visit(item, o)
            if not self.check_type(type_ele, item_type, can_coerce=False):
                raise IllegalArrayLiteral(node)
            
        return ArrayType(type_ele, len(node.value))
    
    def visit_int_literal(self, node: "IntLiteral", o: Any = None) -> Type: return PrimitiveType("int")
    def visit_float_literal(self, node: "FloatLiteral", o: Any = None) -> Type: return PrimitiveType("float")
    def visit_bool_literal(self, node: "BoolLiteral", o: Any = None) -> Type: return PrimitiveType("boolean")
    def visit_string_literal(self, node: "StringLiteral", o: Any = None) -> Type: return PrimitiveType("string")

    def visit_if_statement(self, node: "IfStatement", o: Any = None) -> list[Symbol]:
        typ = self.visit(node.condition, o[1])
        ## TODO       
        if not self.check_type(typ, PrimitiveType("boolean"), can_coerce=False):
            raise TypeMismatchInStatement(node)
        then_scope = []
        then_context = (then_scope, o[1])
        self.visit(node.then_stmt, then_context)
        if node.else_stmt:
            else_scope = []
            else_context = (else_scope, o[1])
            self.visit(node.else_stmt, else_context)

        return o[0] 
    
    def visit_return_statement(self, node: "ReturnStatement", o: Any = None)-> list[Symbol]: 
        typ = self.visit(node.value, o[1])
        ## TODO
        # if not self.method_curr:
        #     raise Must
        expected_type = None
        if isinstance(self.method_curr, MethodDecl):
            expected_type = self.method_curr.return_type
        elif isinstance(self.method_curr, (ConstructorDecl, DestructorDecl)):
            expected_type = PrimitiveType('void')
        
        # 3c. So sánh kiểu
        if not self.check_type(expected_type, typ, can_coerce=True):
            raise TypeMismatchInStatement(node)
        return o[0]

    def visit_nil_literal(self, node: "NilLiteral", o: Any = None) -> Type: return ClassType("") 
   
    def visit_binary_op(self, node: "BinaryOp", o: Any = None) -> Type:
        left_type = self.visit(node.left, o)
        right_type = self.visit(node.right, o)
        op = node.operator

        if op in ["&&", "||"]:
            if not (self.check_type(left_type, PrimitiveType("boolean"), can_coerce=False) and self.check_type(right_type, PrimitiveType("boolean"), can_coerce=False)):
                raise TypeMismatchInExpression(node)
            return PrimitiveType("boolean")
        if op in ["\\", "%"]:
            if not (self.check_type(left_type, PrimitiveType("int"), can_coerce=False) and self.check_type(right_type, PrimitiveType("int"), can_coerce=False)):
                raise TypeMismatchInExpression(node)
            return PrimitiveType("int")
        if op in ["+", "-", "*"]:
            is_left_numeric = self.check_type(PrimitiveType("float"), left_type, can_coerce=True) or self.check_type(PrimitiveType("int"), left_type, can_coerce=True)
            is_right_numeric = self.check_type(PrimitiveType("float"), right_type, can_coerce=True) or self.check_type(PrimitiveType("int"), right_type, can_coerce=True)
            # is_left_string = self.check_type(PrimitiveType("string"), left_type, can_coerce=True) 
            # is_right_string = self.check_type(PrimitiveType("string"), right_type, can_coerce=True) 

            if not (is_left_numeric and is_right_numeric):
                # (Kiểm tra thêm cho '+' nếu ngôn ngữ hỗ trợ nối chuỗi)
                raise TypeMismatchInExpression(node)
            if self.check_type(left_type, PrimitiveType("float")) or self.check_type(right_type, PrimitiveType("float")):
                return PrimitiveType("float")
            return PrimitiveType("int")
        # 2c. Phép toán luôn trả về Float ( / )
        if op == "/":
            # Cả hai vế phải là số (int hoặc float)
            is_left_numeric = self.check_type(PrimitiveType("float"), left_type, can_coerce=True)
            is_right_numeric = self.check_type(PrimitiveType("float"), right_type, can_coerce=True)
        
            if not (is_left_numeric and is_right_numeric):
                raise TypeMismatchInExpression(node)
        
            # Kết quả luôn là float
            return PrimitiveType("float")
        # 3. Toán tử So sánh (Relational) (==, !=, <, >, <=, >=)
        if op in ["==", "!=", "<", ">", "<=", ">="]:
            # Cả hai vế phải là số (int hoặc float)
            # Case A: Check for (int, int)
             # <-- IT PASSES HERE

            # # Case B: Check for (float, float)
             # <-- It also passes (float, float)
            
            # (Kiểm tra thêm cho ==, != nếu hỗ trợ so sánh boolean)
            if op in ["==", "!="]:
                if (self.check_type(left_type, PrimitiveType("boolean"), can_coerce=False) and self.check_type(right_type, PrimitiveType("boolean"), can_coerce=False)):
                    return PrimitiveType("boolean")
                if (self.check_type(left_type, PrimitiveType("float"), can_coerce=False) and self.check_type(right_type, PrimitiveType("float"), can_coerce=False)):
                    raise TypeMismatchInExpression(node)
                elif (self.check_type(left_type, PrimitiveType("float"), can_coerce=False) and self.check_type(right_type, PrimitiveType("int"), can_coerce=False)) or (self.check_type(left_type, PrimitiveType("int"), can_coerce=False) and self.check_type(right_type, PrimitiveType("float"), can_coerce=False)):
                    raise TypeMismatchInExpression(node)
                elif (self.check_type(left_type, PrimitiveType("boolean"), can_coerce=False) and self.check_type(right_type, PrimitiveType("int"), can_coerce=False)) or (self.check_type(left_type, PrimitiveType("int"), can_coerce=False) and self.check_type(right_type, PrimitiveType("boolean"), can_coerce=False)):
                    raise TypeMismatchInExpression(node)
                elif (self.check_type(left_type, PrimitiveType("boolean"), can_coerce=False) and self.check_type(right_type, PrimitiveType("float"), can_coerce=False)) or (self.check_type(left_type, PrimitiveType("float"), can_coerce=False) and self.check_type(right_type, PrimitiveType("boolean"), can_coerce=False)):
                    raise TypeMismatchInExpression(node)
                
            is_left_numeric = self.check_type(PrimitiveType("int"), left_type, can_coerce=False) or self.check_type(PrimitiveType("float"), left_type, can_coerce=False) 
            is_right_numeric = self.check_type(PrimitiveType("int"), right_type, can_coerce=False) or self.check_type(PrimitiveType("float"), right_type, can_coerce=False)
            if is_left_numeric and is_right_numeric:
                return PrimitiveType("boolean")
            
            # Nếu không phải các trường hợp trên

            # Nếu không phải là các trường hợp trên
            raise TypeMismatchInExpression(node)
        
        if op == '^':
            if self.check_type(left_type, PrimitiveType("string"), can_coerce=False) and self.check_type(right_type, PrimitiveType("string"), can_coerce=False):
                return PrimitiveType("string")
        
        raise TypeMismatchInExpression(node)
        
    def visit_unary_op(self, node: "UnaryOp", o: Any = None) -> Type:
        operand_type = self.visit(node.operand, o)
        op = node.operator
        ## TODO
        # 1. Xử lý toán tử '!' (Logical NOT)
        if op == '!':
            # Toán hạng phải là boolean (không ép kiểu)
            if not self.check_type(operand_type, PrimitiveType("boolean"), can_coerce=False):
                raise TypeMismatchInExpression(node)
        
            # Kết quả trả về là boolean
            return PrimitiveType("boolean")

        if op in ['+', '-']:
            # Toán hạng phải là số (int hoặc float)
        
            # Kiểm tra xem có phải là int không
            if self.check_type(operand_type, PrimitiveType("int"), can_coerce=False):
                return PrimitiveType("int") # Kết quả là int
        
            # Kiểm tra xem có phải là float không
            if self.check_type(operand_type, PrimitiveType("float"), can_coerce=False):
                return PrimitiveType("float") # Kết quả là float
            
            # Nếu không phải cả hai
            raise TypeMismatchInExpression(node)

        raise TypeMismatchInExpression(node)
    def visit_object_creation(self, node: "ObjectCreation", o: Any = None) -> Type:
        current_class = next((c for c in self.list_class if c.name == node.class_name), None)
        if not current_class:
            raise UndeclaredClass(node.class_name)
        found = False
        ## TODO
        # 2a. Lấy kiểu của các đối số (args)
        # 'o' là full_env, truyền thẳng vào
        arg_types = [self.visit(arg, o) for arg in node.args]
        # 2b. Tìm ConstructorDecl
        found_constructor = None
        for member in current_class.members:
            if isinstance(member, ConstructorDecl):
                found_constructor = member
            if found_constructor:
            # TRƯỜNG HỢP 1: Tồn tại hàm tạo tường minh (explicit)
        
                param_types = [p.param_type for p in found_constructor.params]
        
                # Kiểm tra số lượng
                if len(arg_types) == len(param_types):
                    # Kiểm tra kiểu
                    is_match = True
                    for (left_param, right_arg) in zip(param_types, arg_types):
                        if not self.check_type(left_param, right_arg, can_coerce=True):
                            is_match = False
                            break
            
                    if is_match:
                        found = True
                        break
        if not found_constructor:
            # TRƯỜNG HỢP 2: Không có hàm tạo tường minh (dùng hàm tạo mặc định)
        
            # Hàm tạo mặc định chỉ hợp lệ khi không có đối số nào được truyền vào
            if len(arg_types) == 0:
                found = True

        # 3. Xử lý kết quả
        if not found:
            # Nếu 'found' vẫn là False, nghĩa là:
            # - Có hàm tạo nhưng kiểu/số lượng không khớp.
            # - Không có hàm tạo nhưng lại gọi với đối số.
            raise TypeMismatchInExpression(node)
        
        return ClassType(node.class_name)


    ##########################
    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Any = None
    ) -> Type:
        return self.visit(node.expr, o)

    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None): pass
    def visit_array_type(self, node: "ArrayType", o: Any = None):  pass
    def visit_class_type(self, node: "ClassType", o: Any = None):
        global_scope = o[-1] 
    
        # Search the *current* global scope for the class name
        found = next(
            filter(lambda sym: sym.name == node.class_name, global_scope),
            None
        )
        
        if not found:
            # When checking 'A b', 'A' is not in [[Symbol('Student')], [Symbol('io')]]
            # This will now correctly raise the error.
            raise UndeclaredClass(node.class_name)
        
        # If found, just return the type node
        return node
    def visit_reference_type(self, node: "ReferenceType", o: Any = None): pass
    def visit_method_call(self, node: "MethodCall", o: Any = None): pass
    def visit_member_access(self, node: "MemberAccess", o: Any = None): pass
    def visit_array_access(self, node: "ArrayAccess", o: Any = None): pass
    def visit_method_invocation(self, node: "MethodInvocationStatement", o: Any = None): 
        return self.visit_method_invocation_statement(node, o)
    def visit_static_method_invocation(self, node, o: Any = None):
        return self.visit_method_invocation_statement(node, o)
    def visit_static_member_access(self, node, o = None): pass

    


    
