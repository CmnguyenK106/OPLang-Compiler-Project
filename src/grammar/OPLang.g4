grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

//--------------------------------------------------------------//
// DECLARATION
program: class_+ EOF;
class_: CLASS ID (EXTENDS ID | ) LPAREN class_member RPAREN;
class_member: member class_member | ;
member: variable | array_decl_attr | method | constructor | destructor; 

variable: (STATIC? FINAL? | FINAL? STATIC?) ele_or_class ref_lit list_assign_attr SEMI;

list_assign_attr: assign_attr COMMA list_assign_attr | assign_attr;
list_assign_var: assign_var COMMA list_assign_var | assign_var;
assign_attr: ID ASSIGN expression | ID;
assign_var: ID ASSIGN expression | ID;

array_decl_attr: final_lit static_lit array_type ref_lit list_assign_attr SEMI;

method: static_lit method_type ID LBRACK list_param? RBRACK block_stmt;
method_type: otype ref_lit | VOID;

constructor: default_cons | copy_cons | userdefined_cons;
default_cons: ID LBRACK RBRACK block_stmt;
copy_cons: ID LBRACK list_param RBRACK block_stmt;
userdefined_cons: ID LBRACK list_param RBRACK block_stmt;

destructor: TILDE ID LBRACK RBRACK block_stmt;

list_param: params SEMI list_param | params;
params: header_param tailer_param;

tailer_param: ID COMMA tailer_param | ID | OTHER;
header_param: otype ref_lit;

otype: element_type | array_type | class_type;

element_type: INT | FLOAT | STRING | BOOLEAN;
array_type: ele_or_class LSBRACK INT_LIT RSBRACK;

class_type: ID;

ele_or_class: element_type | class_type;

static_lit: STATIC?;
final_lit: FINAL?;
ref_lit: REF?;

// EXPRESSION
list_expression: expression COMMA list_expression | expression;
expression: expression1 (LT | GT | LE | GE) expression1 | expression1;
expression1: expression2 (EQ | NE) expression2 | expression2;
expression2: expression2 (OR | AND) expression3 | expression3;
expression3: expression3 (ADD | SUB) expression4 | expression4;
expression4: expression4 (MUL | FLOATDIV | INTDIV | MODULUS) expression5 | expression5;
expression5: expression5 CONCAT expression6 | expression6;
expression6: NOT expression6 | expression7;
expression7: (ADD | SUB) expression7 | expression9;
//expression8: expression8 LSBRACK expression RSBRACK | expression9;
expression9: expression9 LSBRACK expression RSBRACK | expression9 DOT ID (LBRACK list_expression? RBRACK)? | expression10;
//expression9_two: expression9 | expression10;
//expression9: expression9 DOT expression10 | expression10;
expression10: NEW ID LBRACK list_expression? RBRACK | expression11;
expression11: ID
            | THIS
            | OTHER
            | literal
            | array_literal
            | LBRACK expression? RBRACK
            | LPAREN literal RPAREN;

array_literal: LPAREN list_literal RPAREN;
list_literal: literal COMMA list_literal | literal;
literal: TRUE | FALSE | INT_LIT | FLOAT_LIT | STRING_LIT | NIL;


// STATEMENTS
list_statement: statement list_statement | statement;
statement: assign_stmt
         | block_stmt
         | if_stmt 
         | for_stmt  
         | break_stmt
         | continue_stmt
         | return_stmt
         | method_stmt;
decl_stmts: member_decl decl_stmts | member_decl;
member_decl: var_decl | array_decl;
var_decl: final_lit ele_or_class ref_lit list_assign_var SEMI;
array_decl: array_type ref_lit list_assign_var SEMI;
block_stmt: LPAREN decl_stmts? list_statement? RPAREN;
assign_stmt: lhs ASSIGN expression SEMI;
lhs: ID | expression9;
if_stmt: IF expression THEN block_or_stmt else_stmt?;
else_stmt: ELSE block_or_stmt;
for_stmt: FOR ID ASSIGN expression distance expression DO block_or_stmt;
distance: TO | DOWNTO;
block_or_stmt: block_stmt | statement;
break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
return_stmt: RETURN expression? SEMI;
method_stmt: expression9 SEMI;
//static_invoc: ID DOT ID LBRACK list_expression? RBRACK SEMI;
//method_invoc: expression9 DOT ID LBRACK list_expression? RBRACK SEMI;


//--------------------------------LEXER------------------------------//
// KEYWORDS
FINAL: 'final';
BOOLEAN: 'boolean';
BREAK: 'break';
CLASS: 'class';
CONTINUE: 'continue';
DO: 'do';
ELSE: 'else';
EXTENDS: 'extends';
FLOAT: 'float';
IF: 'if';
INT: 'int';
NEW: 'new';
STRING: 'string';
THEN: 'then';
FOR: 'for';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
VOID: 'void';
NIL: 'nil';
THIS: 'this';
STATIC: 'static';
TO: 'to';
DOWNTO: 'downto'; 
OTHER: 'other';

// OPERATORS
ASSIGN  : ':=';
ADD     : '+';
SUB     : '-';
MUL     : '*';
FLOATDIV: '/';
INTDIV  : '\\';
MODULUS : '%';
EQ      : '==';
NE  : '!=';
GT      : '>';
LT      : '<';
LE: '<=';
GE: '>=';
OR: '||';
AND: '&&';
NOT: '!';
CONCAT: '^';
OBJCREATION: NEW;

// Separators
LSBRACK  : '[';
RSBRACK  : ']';
LPAREN  : '{';
RPAREN  : '}';
LBRACK  : '(';
RBRACK  : ')';
SEMI    : ';';
COLON   : ':';
DOT     : '.';
COMMA   : ',';

// Special Characters
TILDE   : '~';
REF     : '&';

// IDENTIFIER
ID: [A-Za-z_] [A-Za-z0-9_]*;

// LITERAL
FLOAT_LIT: DIGIT+ '.' DIGIT* EXP? | DIGIT+ EXP;  
fragment EXP: [eE] [+-]? DIGIT+;
INT_LIT: DIGIT+;
fragment DIGIT: [0-9];
BOOL_LIT: TRUE | FALSE;

STRING_LIT: '"' STR_CHAR* '"' {self.text = self.text[1:-1]};
fragment STR_CHAR: ~["\\\r\n] | ESC_SEQ ;
fragment ESC_SEQ: '\\' [bfrnt"\\];
fragment ESC_ILLEGAL: '\\' ~[bfnrt"\\];

// COMMENT, WHITE SPACE
COMMENT_BLOCK: '/*' .*? '*/' -> skip;

LINE_COMMENT: '#' ~[\r\n]* ( '\r'? '\n' )? -> skip;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 

// ERROR
ERROR_CHAR: . {raise ErrorToken(self.text)};
UNCLOSE_STRING: '"' STR_CHAR* ('\r\n' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[1:])
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[1:])
    else:
        raise UncloseString(self.text[1:])
};
ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    raise IllegalEscape(self.text[1:])
};
//--------------------------------LEXER------------------------------//