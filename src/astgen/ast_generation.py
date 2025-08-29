"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):

    def visitProgram(self, ctx:OPLangParser.ProgramContext):
        return Program([self.visit(i) for i in ctx.class_()])
    
    # class: CLASS ID (EXTENDS ID | ) LPAREN class_member RPAREN;
    def visitClass_(self, ctx:OPLangParser.Class_Context):
        if ctx.EXTENDS():
            return ClassDecl(ctx.ID()[0].getText(), ctx.ID()[1].getText(), self.visit(ctx.class_member()))
        return ClassDecl(ctx.ID()[0].getText(), None, self.visit(ctx.class_member()))
    
    # class_member: member class_member | ;
    def visitClass_member(self, ctx:OPLangParser.Class_memberContext):
        if ctx.class_member():
            return [self.visit(ctx.member())] + self.visit(ctx.class_member())
        return []
    
    # member: variable | array_decl_attr | method | constructor | destructor; 
    def visitMember(self, ctx:OPLangParser.MemberContext):
        return self.visitChildren(ctx)

    # variable: (STATIC? FINAL? | FINAL? STATIC?) ele_or_class ref_lit list_assign_attr SEMI;
    def visitVariable(self, ctx:OPLangParser.VariableContext):
        static_flag = False
        final_flag = False
        if ctx.STATIC():
            static_flag = True
        if ctx.FINAL():
            final_flag = True
        Ref_lit = self.visit(ctx.ref_lit())
        if Ref_lit is not None:
            Atype = ReferenceType(self.visit(ctx.ele_or_class()))
        else:
            Atype = self.visit(ctx.ele_or_class())
        return AttributeDecl(static_flag, final_flag, Atype, self.visit(ctx.list_assign_attr()))

    # var_decl: final_lit ele_or_class ref_lit list_assign_var SEMI;
    def visitVar_decl(self, ctx:OPLangParser.Var_declContext):
        Final_lit = self.visit(ctx.final_lit())
        Ref = self.visit(ctx.ref_lit())
        if Ref is not None:
            Vtype = ReferenceType(self.visit(ctx.ele_or_class()))
        else:
            Vtype = self.visit(ctx.ele_or_class())
        if Final_lit is not None:
            return VariableDecl(True, Vtype, self.visit(ctx.list_assign_var()))
        return VariableDecl(False, Vtype, self.visit(ctx.list_assign_var()))

    # list_assign_attr: assign_attr COMMA list_assign_attr | assign_attr;
    def visitList_assign_attr(self, ctx:OPLangParser.List_assign_attrContext):
        if ctx.list_assign_attr():
            return [self.visit(ctx.assign_attr())] + self.visit(ctx.list_assign_attr())
        return [self.visit(ctx.assign_attr())]
    
    # list_assign_var: assign_var COMMA list_assign_var | assign_var;
    def visitList_assign_var(self, ctx:OPLangParser.List_assign_varContext):
        if ctx.list_assign_var():
            return [self.visit(ctx.assign_var())] + self.visit(ctx.list_assign_var())
        return [self.visit(ctx.assign_var())]
    
    # assign_attr: ID ASSIGN expression | ID;
    def visitAssign_attr(self, ctx:OPLangParser.Assign_attrContext):
        if ctx.expression():
            return Attribute(ctx.ID().getText(), self.visit(ctx.expression()))
        return Attribute(ctx.ID().getText(), None)
    
    # assign_var: ID ASSIGN expression | ID;
    def visitAssign_var(self, ctx:OPLangParser.Assign_varContext):
        if ctx.expression():
            return Variable(ctx.ID().getText(), self.visit(ctx.expression()))
        return Variable(ctx.ID().getText(), None)
    
    # array_decl_attr: final_lit static_lit array_type ref_lit list_assign_attr SEMI;
    def visitArray_decl_attr(self, ctx:OPLangParser.Array_decl_attrContext):
        Ref = self.visit(ctx.ref_lit())
        Sta = self.visit(ctx.static_lit())
        Fi = self.visit(ctx.final_lit())
        if Sta is not None:
            Sta_flag = True
        else: 
            Sta_flag = False
        if Fi is not None:
            Fi_flag = True
        else:
            Fi_flag = False
        if Ref is not None:
            Atype = ReferenceType(self.visit(ctx.array_type()))
            return AttributeDecl(Sta_flag, Fi_flag, Atype, self.visit(ctx.list_assign_attr()))
        return AttributeDecl(Sta_flag, Fi_flag, self.visit(ctx.array_type()), self.visit(ctx.list_assign_attr()))

    
    # array_type: ele_or_class LSBRACK INT_LIT RSBRACK;
    def visitArray_type(self, ctx:OPLangParser.Array_typeContext):
        return ArrayType(self.visit(ctx.ele_or_class()), int(ctx.INT_LIT().getText()))
    
    # method: static_lit method_type ID LBRACK list_param? RBRACK block_stmt;
    def visitMethod(self, ctx:OPLangParser.MethodContext):
        bl_stmt = self.visit(ctx.block_stmt())
        id = ctx.ID().getText()
        Ptype = self.visit(ctx.method_type())
        S_lit = self.visit(ctx.static_lit())
        is_static = False
        if S_lit is not None: 
            is_static = True
        if ctx.list_param():
            return MethodDecl(is_static, Ptype, id, self.visit(ctx.list_param()), bl_stmt)
        return MethodDecl(is_static, Ptype, id, [], bl_stmt)
    
    # method_type: otype ref_lit | VOID;
    def visitMethod_type(self, ctx:OPLangParser.Method_typeContext):
        if ctx.VOID():
            return PrimitiveType('void')
        Ref = self.visit(ctx.ref_lit())
        if Ref is not None:
            return ReferenceType(self.visit(ctx.otype()))
        return self.visit(ctx.otype())
    
    # constructor: default_cons | copy_cons | userdefined_cons;
    def visitConstructor(self, ctx:OPLangParser.ConstructorContext):
        return self.visitChildren(ctx)
    
    # default_cons: ID LBRACK RBRACK block_stmt;
    def visitDefault_cons(self, ctx:OPLangParser.Default_consContext):
        return ConstructorDecl(ctx.ID().getText(), [], self.visit(ctx.block_stmt()))
    
    # copy_cons: ID LBRACK list_param RBRACK block_stmt;
    def visitCopy_cons(self, ctx:OPLangParser.Copy_consContext):
        return ConstructorDecl(ctx.ID().getText(), self.visit(ctx.list_param()), self.visit(ctx.block_stmt()))
    
    # userdefined_cons: ID LBRACK list_param RBRACK block_stmt;
    def visitUserdefined_cons(self, ctx:OPLangParser.Userdefined_consContext):
        return ConstructorDecl(ctx.ID().getText(), self.visit(ctx.list_param()), self.visit(ctx.block_stmt()))
    
    # destructor: TILDE ID LBRACK RBRACK block_stmt;
    def visitDestructor(self, ctx:OPLangParser.DestructorContext):
        return DestructorDecl(ctx.ID().getText(), self.visit(ctx.block_stmt()))
    
    # list_param: params SEMI list_param | params;
    def visitList_param(self, ctx:OPLangParser.List_paramContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.params())
        return self.visit(ctx.params()) + self.visit(ctx.list_param())
    
    # params: header_param tailer_param;
    def visitParams(self, ctx:OPLangParser.ParamsContext):
        Ptype = self.visit(ctx.header_param())
        lst_id = self.visit(ctx.tailer_param())

        return list(map(lambda x: Parameter(Ptype, x), lst_id))
    
    # tailer_param: ID COMMA tailer_param | ID | OTHER;
    def visitTailer_param(self, ctx:OPLangParser.Tailer_paramContext):
        if ctx.getChildCount() == 1:
            if ctx.ID():
                return [ctx.ID().getText()]
            elif ctx.OTHER():
                return [ctx.OTHER().getText()]
        return [ctx.ID().getText()] + self.visit(ctx.tailer_param())
    
    # header_param: otype ref_lit;
    def visitHeader_param(self, ctx:OPLangParser.Header_paramContext):
        Ref = self.visit(ctx.ref_lit())
        if Ref is not None:
            return ReferenceType(self.visit(ctx.otype()))
        return self.visit(ctx.otype())
    
    # otype: element_type | array_type | class_type;
    def visitOtype(self, ctx:OPLangParser.OtypeContext):
        if ctx.element_type():
            return self.visit(ctx.element_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        return self.visit(ctx.class_type())
    
    # ele_or_class: element_type | class_type;
    def visitEle_or_class(self, ctx:OPLangParser.Ele_or_classContext):
        if ctx.element_type():
            return self.visit(ctx.element_type())
        return self.visit(ctx.class_type())
    
    # element_type: INT | FLOAT | STRING | BOOLEAN;
    def visitElement_type(self, ctx:OPLangParser.Element_typeContext):
        if ctx.INT():
            return PrimitiveType('int')
        elif ctx.FLOAT():
            return PrimitiveType('float')
        elif ctx.BOOLEAN():
            return PrimitiveType('boolean')
        return PrimitiveType('string')
    
    # class_type: ID;
    def visitClass_type(self, ctx:OPLangParser.Class_typeContext):
        return ClassType(ctx.ID().getText())
    
    # static_lit: STATIC?;
    def visitStatic_lit(self, ctx:OPLangParser.Static_litContext):
        if ctx.STATIC():
            return ctx.STATIC().getText()
        return None

    # final_lit: FINAL?;
    def visitFinal_lit(self, ctx:OPLangParser.Final_litContext):
        if ctx.FINAL():
            return ctx.FINAL().getText()
        return None
    
    # ref_lit: REF?;
    def visitRef_lit(self, ctx:OPLangParser.Ref_litContext):
        if ctx.REF():
            return ctx.REF().getText()
        return None
    
    # EXPRESSION

    # list_expression: expression COMMA list_expression | expression;
    def visitList_expression(self, ctx:OPLangParser.List_expressionContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expression())]
        return [self.visit(ctx.expression())] + self.visit(ctx.list_expression())
    
    # expression: expression1 (LT | GT | LE | GE) expression1 | expression1;
    def visitExpression(self, ctx:OPLangParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression1()[0])
        return BinaryOp(self.visit(ctx.expression1()[0]), ctx.getChild(1).getText(), self.visit(ctx.expression1()[1]))
    
    # expression1: expression2 (EQ | NE) expression2 | expression2;
    def visitExpression1(self, ctx:OPLangParser.Expression1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression2()[0])
        return BinaryOp(self.visit(ctx.expression2()[0]), ctx.getChild(1).getText(), self.visit(ctx.expression2()[1]))
    
    # expression2: expression2 (OR | AND) expression3 | expression3;
    def visitExpression2(self, ctx:OPLangParser.Expression2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression3())
        return BinaryOp(self.visit(ctx.expression2()), ctx.getChild(1).getText(), self.visit(ctx.expression3()))
    
    # expression3: expression3 (ADD | SUB) expression4 | expression4;
    def visitExpression3(self, ctx:OPLangParser.Expression3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression4())
        return BinaryOp(self.visit(ctx.expression3()), ctx.getChild(1).getText(), self.visit(ctx.expression4()))
    
    # expression4: expression4 (MUL | FLOATDIV | INTDIV | MODULUS) expression5 | expression5;
    def visitExpression4(self, ctx:OPLangParser.Expression4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression5())
        return BinaryOp(self.visit(ctx.expression4()), ctx.getChild(1).getText(), self.visit(ctx.expression5()))
    
    # expression5: expression5 CONCAT expression6 | expression6;
    def visitExpression5(self, ctx:OPLangParser.Expression5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression6())
        return BinaryOp(self.visit(ctx.expression5()), ctx.getChild(1).getText(), self.visit(ctx.expression6()))
    
    # expression6: NOT expression6 | expression7;
    def visitExpression6(self, ctx:OPLangParser.Expression6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression7())
        return UnaryOp(ctx.NOT().getText(), self.visit(ctx.expression6()))
    
    # expression7: (ADD | SUB) expression7 | expression9;
    def visitExpression7(self, ctx:OPLangParser.Expression7Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression9())
        return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.expression7()))
    
    # expression9: expression9 LSBRACK expression RSBRACK | ID DOT ID (LBRACK list_expression? RBRACK)? | expression9 DOT ID (LBRACK list_expression? RBRACK)? | expression10;
    def visitExpression9(self, ctx:OPLangParser.Expression9Context):
        if ctx.getChildCount() > 1:
            primary = self.visit(ctx.expression9())
            if ctx.list_expression():
                post_op = MethodCall(ctx.ID().getText(), self.visit(ctx.list_expression()))
                #return PostfixExpression(self.visit(ctx.expression9()), [MethodCall(ctx.ID(), self.visit(ctx.list_expression()))])
            elif ctx.LBRACK():
                post_op = MethodCall(ctx.ID().getText(), [])
                # return PostfixExpression(self.visit(ctx.expression9()), [MethodCall(ctx.ID(), [])])
            elif ctx.LSBRACK():
                post_op = ArrayAccess(self.visit(ctx.expression()))
            else: 
                if ctx.getChildCount() > 1:
                    post_op = MemberAccess(ctx.ID().getText())
                    # return PostfixExpression(self.visit(ctx.expression9()), [MemberAccess(ctx.ID().getText())])
            return (lambda p, o: (p.postfix_ops.append(o) or p if isinstance(p, PostfixExpression) else PostfixExpression(p, [o])))(primary, post_op)
        return self.visit(ctx.expression10())
    
    # expression10: NEW ID LBRACK list_expression? RBRACK | expression11;
    def visitExpression10(self, ctx:OPLangParser.Expression10Context):
        if ctx.NEW():   
            if ctx.list_expression():
                return ObjectCreation(ctx.ID().getText(), self.visit(ctx.list_expression()))
            else: 
                return ObjectCreation(ctx.ID().getText(), [])
        return self.visit(ctx.expression11())
        
    
    """ expression11: ID
            | THIS
            | OTHER
            | literal
            | array_literal
            | LBRACK expression? RBRACK
            | LPAREN literal RPAREN; """
    def visitExpression11(self, ctx:OPLangParser.Expression11Context):
        if ctx.expression():
            return ParenthesizedExpression(self.visit(ctx.expression()))
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.THIS():
            return ThisExpression()
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.OTHER():
            return Identifier("other")
        return self.visitChildren(ctx)
    
    """LITERAL"""

    # array_literal: LPAREN list_literal RPAREN;
    def visitArray_literal(self, ctx:OPLangParser.Array_literalContext):
        return ArrayLiteral(self.visit(ctx.list_literal()))
    
    # list_literal: literal COMMA list_literal | literal
    def visitList_literal(self, ctx:OPLangParser.List_literalContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.literal())]
        return [self.visit(ctx.literal())] + self.visit(ctx.list_literal())
    
    # literal: TRUE | FALSE | INT_LIT | FLOAT_LIT | STRING_LIT | NIL;
    def visitLiteral(self, ctx:OPLangParser.LiteralContext):
        if ctx.TRUE():
            return BoolLiteral(True)
        elif ctx.FALSE():
            return BoolLiteral(False)
        elif ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        return NilLiteral()
    
    """ STATEMENTS """

    # list_statement: statement list_statement | statement;
    def visitList_statement(self, ctx:OPLangParser.List_statementContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.statement())]
        return [self.visit(ctx.statement())] + self.visit(ctx.list_statement())
    
    """ statement: assign_stmt
         | block_stmt
         | if_stmt 
         | for_stmt  
         | break_stmt 
         | continue_stmt 
         | return_stmt 
         | method_stmt;
    """
    def visitStatement(self, ctx:OPLangParser.StatementContext):
        return self.visitChildren(ctx)
    
    
    # decl_stmts: member_decl decl_stmts | member_decl;
    def visitDecl_stmts(self, ctx:OPLangParser.Decl_stmtsContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.member_decl())]
        return [self.visit(ctx.member_decl())] + self.visit(ctx.decl_stmts())
    
    # member_decl: var_decl | array_decl;
    def visitMember_decl(self, ctx:OPLangParser.Member_declContext):
        return self.visitChildren(ctx)
    
    # array_decl: array_type ref_lit list_assign_var SEMI;
    def visitArray_decl(self, ctx:OPLangParser.Array_declContext):
        Ref = self.visit(ctx.ref_lit())
        if Ref is not None:
            Atype = ReferenceType(self.visit(ctx.array_type()))
            return VariableDecl(False, Atype, self.visit(ctx.list_assign_var()))
        return VariableDecl(False, self.visit(ctx.array_type()), self.visit(ctx.list_assign_var()))
    
    # block_stmt: LPAREN decl_stmts? list_statement? RPAREN;
    def visitBlock_stmt(self, ctx:OPLangParser.Block_stmtContext):
        if ctx.decl_stmts():
            if ctx.list_statement():
                return BlockStatement(self.visit(ctx.decl_stmts()), self.visit(ctx.list_statement()))
            else:
                return BlockStatement(self.visit(ctx.decl_stmts()), [])
        if ctx.list_statement():
            return BlockStatement([], self.visit(ctx.list_statement()))
        return BlockStatement([], [])
    
    # assign_stmt: lhs ASSIGN expression SEMI;
    def visitAssign_stmt(self, ctx:OPLangParser.Assign_stmtContext):
        return AssignmentStatement(self.visit(ctx.lhs()), self.visit(ctx.expression()))
    
    # lhs: ID | expression9;
    def visitLhs(self, ctx:OPLangParser.LhsContext):
        if ctx.ID():
            return IdLHS(ctx.ID().getText())
        # elif ctx.LSBRACK():
        #     return PostfixLHS(PostfixExpression(self.visit(ctx.expression8()), [ArrayAccess(self.visit(ctx.expression()))]))
        return PostfixLHS(self.visit(ctx.expression9()))
    
    # if_stmt: IF expression THEN block_or_stmt else_stmt?;
    def visitIf_stmt(self, ctx:OPLangParser.If_stmtContext):
        if ctx.else_stmt():
            return IfStatement(self.visit(ctx.expression()), self.visit(ctx.block_or_stmt()), self.visit(ctx.else_stmt()))
        return IfStatement(self.visit(ctx.expression()), self.visit(ctx.block_or_stmt()), None)
    
    # else_stmt: ELSE block_or_stmt;
    def visitElse_stmt(self, ctx:OPLangParser.Else_stmtContext):
        return self.visit(ctx.block_or_stmt())
    
    # for_stmt: FOR ID ASSIGN expression distance expression DO block_or_stmt;
    def visitFor_stmt(self, ctx:OPLangParser.For_stmtContext):
        return ForStatement(ctx.ID().getText(),self.visit(ctx.expression()[0]), self.visit(ctx.distance()), self.visit(ctx.expression()[1]), self.visit(ctx.block_or_stmt()))
    
    # distance: TO | DOWNTO;
    def visitDistance(self, ctx:OPLangParser.DistanceContext):
        if ctx.TO():
            return ctx.TO().getText()
        return ctx.DOWNTO().getText()
    
    # block_or_stmt: block_stmt | statement;
    def visitBlock_or_stmt(self, ctx:OPLangParser.Block_or_stmtContext):
        if ctx.block_stmt():
            return self.visit(ctx.block_stmt())
        return self.visit(ctx.statement())

    # break_stmt: BREAK SEMI;
    def visitBreak_stmt(self, ctx:OPLangParser.Break_stmtContext):
        return BreakStatement()
    
    # continue_stmt: CONTINUE SEMI;
    def visitContinue_stmt(self, ctx:OPLangParser.Continue_stmtContext):
        return ContinueStatement()
    
    # return_stmt: RETURN expression? SEMI;
    def visitReturn_stmt(self, ctx:OPLangParser.Return_stmtContext):
        if ctx.expression():
            return ReturnStatement(self.visit(ctx.expression()))
        return ReturnStatement(NilLiteral())
    
    # method_stmt: expression9 SEMI;
    def visitMethod_stmt(self, ctx:OPLangParser.Method_stmtContext):
        return MethodInvocationStatement(self.visit(ctx.expression9()))
