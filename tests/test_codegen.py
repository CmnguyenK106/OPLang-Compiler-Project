"""
Test cases for OPLang code generation.
This file contains test cases for the code generator.
Students should add more test cases here.
"""

from src.utils.nodes import *
from utils import CodeGenerator


def test_001():
    """Test basic class with main method and print statement"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,  # is_static
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [StringLiteral("Hello World")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test integer literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [IntLiteral(42)])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test float literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [FloatLiteral(3.14)])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test boolean literal - true"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BoolLiteral(True)])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test boolean literal - false"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BoolLiteral(False)])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test nil literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [StringLiteral("nil")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "nil"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test variable declaration with initialization"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("x")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test variable assignment"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(5))])
                    ], [
                        AssignmentStatement(IdLHS("x"), IntLiteral(20)),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("x")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test binary operation - addition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(IntLiteral(5), "+", IntLiteral(3))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test binary operation - subtraction"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(IntLiteral(10), "-", IntLiteral(4))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011():
    """Test binary operation - multiplication"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(IntLiteral(6), "*", IntLiteral(7))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_012():
    """Test binary operation - division"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(IntLiteral(20), "/", IntLiteral(4))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_013():
    """Test if statement without else - true condition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        IfStatement(
                            BoolLiteral(True),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("yes")])]
                                    )
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_014():
    """Test if statement with else - true condition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        IfStatement(
                            BoolLiteral(True),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("true")])]
                                    )
                                )
                            ]),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("false")])]
                                    )
                                )
                            ])
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_015():
    """Test if statement with else - false condition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        IfStatement(
                            BoolLiteral(False),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("true")])]
                                    )
                                )
                            ]),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("false")])]
                                    )
                                )
                            ])
                        )
                    ])
                )
            ]
        )
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_016():
    """Test if statement with comparison"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        IfStatement(
                            BinaryOp(IntLiteral(5), ">", IntLiteral(3)),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("greater")])]
                                    )
                                )
                            ]),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("less")])]
                                    )
                                )
                            ])
                        )
                    ])
                )
            ]
        )
    ])
    expected = "greater"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_017():
    """Test for loop - simple iteration (to)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(5),
                            BlockStatement([], [
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_018():
    """Test for loop - downto"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(5),
                            "downto",
                            IntLiteral(1),
                            BlockStatement([], [
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_019():
    """Test for loop with break"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(10),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(Identifier("i"), ">", IntLiteral(3)),
                                    BreakStatement(),
                                    None
                                ),
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
    """Test for loop with continue"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(5),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(Identifier("i"), "==", IntLiteral(3)),
                                    ContinueStatement(),
                                    None
                                ),
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_021():
    """Test nested if statements"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))])
                    ], [
                        IfStatement(
                            BinaryOp(Identifier("x"), ">", IntLiteral(5)),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(Identifier("x"), "<", IntLiteral(15)),
                                    BlockStatement([], [
                                        MethodInvocationStatement(
                                            PostfixExpression(
                                                Identifier("io"),
                                                [MethodCall("writeStr", [StringLiteral("between")])]
                                            )
                                        )
                                    ]),
                                    None
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "between"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_022():
    """Test for loop printing values"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(3),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeInt", [Identifier("i")])]
                                    )
                                )
                            ])
                        )
                    ])
                )
            ]
        )
    ])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_023():
    """Test static method call with return value"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "getValue",
                    [],
                    BlockStatement([], [
                        ReturnStatement(IntLiteral(42))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("getValue", [])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_024():
    """Test static method call with parameters"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "add",
                    [Parameter(PrimitiveType("int"), "a"), Parameter(PrimitiveType("int"), "b")],
                    BlockStatement([], [
                        ReturnStatement(BinaryOp(Identifier("a"), "+", Identifier("b")))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("add", [IntLiteral(10), IntLiteral(20)])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_025():
    """Test method calling another method"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "getBase",
                    [],
                    BlockStatement([], [
                        ReturnStatement(IntLiteral(5))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "double",
                    [],
                    BlockStatement([], [
                        ReturnStatement(
                            BinaryOp(
                                PostfixExpression(Identifier("Main"), [MethodCall("getBase", [])]),
                                "*",
                                IntLiteral(2)
                            )
                        )
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(Identifier("Main"), [MethodCall("double", [])])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_026():
    """Test method with void return"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "printMessage",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [StringLiteral("hello")])]
                            )
                        )
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("Main"),
                                [MethodCall("printMessage", [])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027():
    """Test method with multiple parameters"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "sum3",
                    [
                        Parameter(PrimitiveType("int"), "a"),
                        Parameter(PrimitiveType("int"), "b"),
                        Parameter(PrimitiveType("int"), "c")
                    ],
                    BlockStatement([], [
                        ReturnStatement(
                            BinaryOp(
                                BinaryOp(Identifier("a"), "+", Identifier("b")),
                                "+",
                                Identifier("c")
                            )
                        )
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("sum3", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_028():
    """Test method returning boolean"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("boolean"),
                    "isPositive",
                    [Parameter(PrimitiveType("int"), "x")],
                    BlockStatement([], [
                        ReturnStatement(BinaryOp(Identifier("x"), ">", IntLiteral(0)))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("isPositive", [IntLiteral(5)])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_029():
    """Test method returning string"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("string"),
                    "getMessage",
                    [],
                    BlockStatement([], [
                        ReturnStatement(StringLiteral("test"))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("getMessage", [])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "test"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_030():
    """Test method with float parameter and return"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("float"),
                    "half",
                    [Parameter(PrimitiveType("float"), "x")],
                    BlockStatement([], [
                        ReturnStatement(BinaryOp(Identifier("x"), "/", FloatLiteral(2.0)))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [
                                    PostfixExpression(
                                        Identifier("Main"),
                                        [MethodCall("half", [FloatLiteral(10.0)])]
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "5.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    """Test binary operation - modulus"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(IntLiteral(17), "%", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_032():
    """Test binary operation - equality"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(IntLiteral(5), "==", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_033():
    """Test binary operation - inequality"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(IntLiteral(5), "!=", IntLiteral(3))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    """Test binary operation - less than"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(IntLiteral(3), "<", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_035():
    """Test binary operation - less than or equal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(IntLiteral(5), "<=", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036():
    """Test binary operation - greater than or equal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(IntLiteral(7), ">=", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_037():
    """Test binary operation - logical AND (true)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(BoolLiteral(True), "&&", BoolLiteral(True))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_038():
    """Test binary operation - logical AND (false)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(BoolLiteral(True), "&&", BoolLiteral(False))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_039():
    """Test binary operation - logical OR (true)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(BoolLiteral(True), "||", BoolLiteral(False))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040():
    """Test binary operation - logical OR (false)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [BinaryOp(BoolLiteral(False), "||", BoolLiteral(False))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_041():
    """Test unary operation - negation"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [UnaryOp("-", IntLiteral(5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_042():
    """Test unary operation - positive"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [UnaryOp("+", IntLiteral(7))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043():
    """Test unary operation - logical NOT (true to false)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [UnaryOp("!", BoolLiteral(True))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044():
    """Test unary operation - logical NOT (false to true)"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [UnaryOp("!", BoolLiteral(False))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045():
    """Test return statement with value"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("int"),
                    "compute",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))])
                    ], [
                        ReturnStatement(BinaryOp(Identifier("x"), "*", IntLiteral(3)))
                    ])
                ),
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(Identifier("Main"), [MethodCall("compute", [])])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_046():
    """Test float addition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [BinaryOp(FloatLiteral(2.5), "+", FloatLiteral(1.5))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "4.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_047():
    """Test multiple variable declarations"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("a", IntLiteral(1))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("b", IntLiteral(2))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("c", IntLiteral(3))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    BinaryOp(
                                        BinaryOp(Identifier("a"), "+", Identifier("b")),
                                        "+",
                                        Identifier("c")
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_048():
    """Test complex arithmetic expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    BinaryOp(
                                        BinaryOp(IntLiteral(10), "+", IntLiteral(5)),
                                        "*",
                                        BinaryOp(IntLiteral(8), "-", IntLiteral(3))
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "75"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_049():
    """Test nested if with else"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(20))])
                    ], [
                        IfStatement(
                            BinaryOp(Identifier("x"), ">", IntLiteral(15)),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(Identifier("x"), ">", IntLiteral(25)),
                                    BlockStatement([], [
                                        MethodInvocationStatement(
                                            PostfixExpression(
                                                Identifier("io"),
                                                [MethodCall("writeStr", [StringLiteral("large")])]
                                            )
                                        )
                                    ]),
                                    BlockStatement([], [
                                        MethodInvocationStatement(
                                            PostfixExpression(
                                                Identifier("io"),
                                                [MethodCall("writeStr", [StringLiteral("medium")])]
                                            )
                                        )
                                    ])
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "medium"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_050():
    """Test for loop with arithmetic operations"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("result", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(4),
                            BlockStatement([], [
                                AssignmentStatement(
                                    IdLHS("result"),
                                    BinaryOp(Identifier("result"), "+", BinaryOp(Identifier("i"), "*", IntLiteral(2)))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("result")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_051():
    """Test boolean expression with multiple conditions"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("a", IntLiteral(5))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("b", IntLiteral(10))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("c", IntLiteral(15))])
                    ], [
                        IfStatement(
                            BinaryOp(
                                BinaryOp(Identifier("a"), "<", Identifier("b")),
                                "&&",
                                BinaryOp(Identifier("b"), "<", Identifier("c"))
                            ),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("ascending")])]
                                    )
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "ascending"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_052():
    """Test array access with variable index"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, ArrayType(PrimitiveType("int"), 3), [
                            Variable("arr", ArrayLiteral([IntLiteral(5), IntLiteral(10), IntLiteral(15)]))
                        ]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("index", IntLiteral(0))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(Identifier("arr"), [ArrayAccess(Identifier("index"))])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_053():
    """Test multiple breaks in loop"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("count", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(20),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(Identifier("i"), ">", IntLiteral(7)),
                                    BreakStatement(),
                                    None
                                ),
                                AssignmentStatement(
                                    IdLHS("count"),
                                    BinaryOp(Identifier("count"), "+", IntLiteral(1))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("count")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_054():
    """Test continue with condition"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(10),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                                    ContinueStatement(),
                                    None
                                ),
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_055():
    """Test nested for loops"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("j", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(3),
                            BlockStatement([], [
                                ForStatement(
                                    "j",
                                    IntLiteral(1),
                                    "to",
                                    IntLiteral(2),
                                    BlockStatement([], [
                                        AssignmentStatement(
                                            IdLHS("sum"),
                                            BinaryOp(Identifier("sum"), "+", IntLiteral(1))
                                        )
                                    ])
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_056():
    """Test multiple variable assignments"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(5))])
                    ], [
                        AssignmentStatement(IdLHS("x"), IntLiteral(10)),
                        AssignmentStatement(IdLHS("x"), BinaryOp(Identifier("x"), "+", IntLiteral(5))),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("x")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_057():
    """Test complex condition in if statement"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(8))])
                    ], [
                        IfStatement(
                            BinaryOp(
                                BinaryOp(Identifier("x"), ">", IntLiteral(5)),
                                "&&",
                                BinaryOp(BinaryOp(Identifier("x"), "%", IntLiteral(2)), "==", IntLiteral(0))
                            ),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("even and greater")])]
                                    )
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "even and greater"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_058():
    """Test variable declaration with int literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("num", IntLiteral(42))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("num")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_059():
    """Test variable declaration with float literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("float"), [Variable("pi", FloatLiteral(3.14))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [Identifier("pi")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_060():
    """Test variable declaration with boolean literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [Variable("flag", BoolLiteral(True))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("flag")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_061():
    """Test variable declaration with string literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("string"), [Variable("msg", StringLiteral("world"))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [Identifier("msg")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "world"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_062():
    """Test variable assignment to new value"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(5))])
                    ], [
                        AssignmentStatement(IdLHS("x"), IntLiteral(20)),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("x")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_063():
    """Test variable assignment with expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("a", IntLiteral(3))])
                    ], [
                        AssignmentStatement(IdLHS("a"), BinaryOp(Identifier("a"), "+", IntLiteral(7))),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("a")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_064():
    """Test multiple int variables"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(10))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("y", IntLiteral(20))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [BinaryOp(Identifier("x"), "+", Identifier("y"))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_065():
    """Test variable with negative value"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("neg", UnaryOp("-", IntLiteral(15)))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("neg")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "-15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_066():
    """Test variable with arithmetic expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [
                            Variable("result", BinaryOp(IntLiteral(6), "*", IntLiteral(7)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("result")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_067():
    """Test reassigning variable multiple times"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("val", IntLiteral(1))])
                    ], [
                        AssignmentStatement(IdLHS("val"), IntLiteral(2)),
                        AssignmentStatement(IdLHS("val"), IntLiteral(3)),
                        AssignmentStatement(IdLHS("val"), IntLiteral(4)),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("val")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_068():
    """Test float variable assignment"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("float"), [Variable("f", FloatLiteral(1.5))])
                    ], [
                        AssignmentStatement(IdLHS("f"), FloatLiteral(2.5)),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [Identifier("f")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_069():
    """Test boolean variable assignment"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [Variable("flag", BoolLiteral(False))])
                    ], [
                        AssignmentStatement(IdLHS("flag"), BoolLiteral(True)),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("flag")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_070():
    """Test string variable assignment"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("string"), [Variable("s", StringLiteral("old"))])
                    ], [
                        AssignmentStatement(IdLHS("s"), StringLiteral("new")),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [Identifier("s")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "new"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_071():
    """Test variable with comparison expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [
                            Variable("isGreater", BinaryOp(IntLiteral(10), ">", IntLiteral(5)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("isGreater")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_072():
    """Test variable swap using temp"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("a", IntLiteral(5))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("b", IntLiteral(10))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("temp", IntLiteral(0))])
                    ], [
                        AssignmentStatement(IdLHS("temp"), Identifier("a")),
                        AssignmentStatement(IdLHS("a"), Identifier("b")),
                        AssignmentStatement(IdLHS("b"), Identifier("temp")),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("a")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_073():
    """Test variable initialization with zero"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("zero", IntLiteral(0))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("zero")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_074():
    """Test variable with division result"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [
                            Variable("quotient", BinaryOp(IntLiteral(20), "/", IntLiteral(4)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("quotient")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_075():
    """Test variable with modulo result"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [
                            Variable("remainder", BinaryOp(IntLiteral(13), "%", IntLiteral(4)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("remainder")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_076():
    """Test increment variable by itself"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("counter", IntLiteral(5))])
                    ], [
                        AssignmentStatement(IdLHS("counter"), BinaryOp(Identifier("counter"), "+", IntLiteral(1))),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("counter")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_077():
    """Test decrement variable by itself"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("counter", IntLiteral(10))])
                    ], [
                        AssignmentStatement(IdLHS("counter"), BinaryOp(Identifier("counter"), "-", IntLiteral(1))),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("counter")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_078():
    """Test multiply variable by itself"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("val", IntLiteral(3))])
                    ], [
                        AssignmentStatement(IdLHS("val"), BinaryOp(Identifier("val"), "*", Identifier("val"))),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("val")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_079():
    """Test three variables with expressions"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(2))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("y", IntLiteral(3))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("z", BinaryOp(Identifier("x"), "*", Identifier("y")))])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("z")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_080():
    """Test variable with logical AND"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [
                            Variable("result", BinaryOp(BoolLiteral(True), "&&", BoolLiteral(True)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("result")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_081():
    """Test variable with logical OR"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [
                            Variable("result", BinaryOp(BoolLiteral(False), "||", BoolLiteral(True)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("result")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_082():
    """Test variable with negation"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [
                            Variable("opposite", UnaryOp("!", BoolLiteral(False)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("opposite")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_083():
    """Test chain of assignments"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("a", IntLiteral(1))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("b", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("c", IntLiteral(0))])
                    ], [
                        AssignmentStatement(IdLHS("b"), Identifier("a")),
                        AssignmentStatement(IdLHS("c"), Identifier("b")),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("c")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084():
    """Test float variable with subtraction"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("float"), [
                            Variable("diff", BinaryOp(FloatLiteral(10.5), "-", FloatLiteral(3.5)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [Identifier("diff")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "7.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_085():
    """Test float variable with multiplication"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("float"), [
                            Variable("product", BinaryOp(FloatLiteral(2.5), "*", FloatLiteral(4.0)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [Identifier("product")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_086():
    """Test variable with equality check"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [
                            Variable("isEqual", BinaryOp(IntLiteral(7), "==", IntLiteral(7)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeBool", [Identifier("isEqual")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_087():
    """Test variable assignment from another variable"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("original", IntLiteral(100))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("copy", IntLiteral(0))])
                    ], [
                        AssignmentStatement(IdLHS("copy"), Identifier("original")),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("copy")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_088():
    """Test array element assignment"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, ArrayType(PrimitiveType("int"), 3), [
                            Variable("arr", ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)]))
                        ])
                    ], [
                        AssignmentStatement(
                            PostfixLHS(PostfixExpression(Identifier("arr"), [ArrayAccess(IntLiteral(1))])),
                            IntLiteral(10)
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(Identifier("arr"), [ArrayAccess(IntLiteral(1))])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_089():
    """Test string array literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, ArrayType(PrimitiveType("string"), 2), [
                            Variable("words", ArrayLiteral([StringLiteral("hello"), StringLiteral("world")]))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeStr", [
                                    PostfixExpression(Identifier("words"), [ArrayAccess(IntLiteral(0))])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_090():
    """Test if statement with boolean variable"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [Variable("check", BoolLiteral(True))])
                    ], [
                        IfStatement(
                            Identifier("check"),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("yes")])]
                                    )
                                )
                            ]),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("no")])]
                                    )
                                )
                            ])
                        )
                    ])
                )
            ]
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_091():
    """Test for loop counting down with step"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("sum", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(10),
                            "downto",
                            IntLiteral(5),
                            BlockStatement([], [
                                AssignmentStatement(
                                    IdLHS("sum"),
                                    BinaryOp(Identifier("sum"), "+", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("sum")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "45"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_092():
    """Test float division"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeFloat", [BinaryOp(FloatLiteral(10.0), "/", FloatLiteral(4.0))])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_093():
    """Test comparison operators in sequence"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(7))])
                    ], [
                        IfStatement(
                            BinaryOp(
                                BinaryOp(Identifier("x"), ">=", IntLiteral(5)),
                                "&&",
                                BinaryOp(Identifier("x"), "<=", IntLiteral(10))
                            ),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("range")])]
                                    )
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "range"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_094():
    """Test complex nested expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    BinaryOp(
                                        BinaryOp(
                                            BinaryOp(IntLiteral(2), "+", IntLiteral(3)),
                                            "*",
                                            IntLiteral(4)
                                        ),
                                        "-",
                                        IntLiteral(5)
                                    )
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_095():
    """Test empty array literal"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, ArrayType(PrimitiveType("int"), 1), [
                            Variable("arr", ArrayLiteral([IntLiteral(99)]))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [
                                    PostfixExpression(Identifier("arr"), [ArrayAccess(IntLiteral(0))])
                                ])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_096():
    """Test conditional with NOT operator"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("boolean"), [Variable("flag", BoolLiteral(False))])
                    ], [
                        IfStatement(
                            UnaryOp("!", Identifier("flag")),
                            BlockStatement([], [
                                MethodInvocationStatement(
                                    PostfixExpression(
                                        Identifier("io"),
                                        [MethodCall("writeStr", [StringLiteral("not set")])]
                                    )
                                )
                            ]),
                            None
                        )
                    ])
                )
            ]
        )
    ])
    expected = "not set"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_097():
    """Test for loop with multiplication in body"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("product", IntLiteral(1))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(2),
                            "to",
                            IntLiteral(4),
                            BlockStatement([], [
                                AssignmentStatement(
                                    IdLHS("product"),
                                    BinaryOp(Identifier("product"), "*", Identifier("i"))
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("product")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "24"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_098():
    """Test multiple sequential if statements"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("x", IntLiteral(5))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("count", IntLiteral(0))])
                    ], [
                        IfStatement(
                            BinaryOp(Identifier("x"), ">", IntLiteral(0)),
                            BlockStatement([], [
                                AssignmentStatement(IdLHS("count"), BinaryOp(Identifier("count"), "+", IntLiteral(1)))
                            ]),
                            None
                        ),
                        IfStatement(
                            BinaryOp(Identifier("x"), "<", IntLiteral(10)),
                            BlockStatement([], [
                                AssignmentStatement(IdLHS("count"), BinaryOp(Identifier("count"), "+", IntLiteral(1)))
                            ]),
                            None
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("count")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_099():
    """Test variable with subtraction expression"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [
                            Variable("diff", BinaryOp(IntLiteral(50), "-", IntLiteral(18)))
                        ])
                    ], [
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("diff")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "32"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_100():
    """Test for loop with if statement inside"""
    ast = Program([
        ClassDecl(
            "Main",
            None,
            [
                MethodDecl(
                    True,
                    PrimitiveType("void"),
                    "main",
                    [],
                    BlockStatement([
                        VariableDecl(False, PrimitiveType("int"), [Variable("count", IntLiteral(0))]),
                        VariableDecl(False, PrimitiveType("int"), [Variable("i", None)])
                    ], [
                        ForStatement(
                            "i",
                            IntLiteral(1),
                            "to",
                            IntLiteral(10),
                            BlockStatement([], [
                                IfStatement(
                                    BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(3)), "==", IntLiteral(0)),
                                    BlockStatement([], [
                                        AssignmentStatement(
                                            IdLHS("count"),
                                            BinaryOp(Identifier("count"), "+", IntLiteral(1))
                                        )
                                    ]),
                                    None
                                )
                            ])
                        ),
                        MethodInvocationStatement(
                            PostfixExpression(
                                Identifier("io"),
                                [MethodCall("writeInt", [Identifier("count")])]
                            )
                        )
                    ])
                )
            ]
        )
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# TODO: Add more test cases here
# Students should implement at least 100 test cases covering:
# - All literal types (int, float, boolean, string, array, nil)
# - Variable declarations and assignments
# - Binary operations (+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||)
# - Unary operations (-, +, !)
# - Control flow (if, for, break, continue)
# - Return statements
# - Method calls (static and instance)
# - Member access
# - Array access
# - Object creation
# - This expression
# - Constructors and destructors
# - Inheritance and polymorphism

