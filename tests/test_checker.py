from utils import Checker


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_005():
    source = """
class io {}
class votien{static void main(){}}
"""
    expected = "Redeclared(Class, io)"
    assert Checker(source).check_from_source() == expected

def test_006():
    source = """
class test {
    int a := 1, b, a;
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected

def test_007():
    source = """
class test {
    int a := 1;
    void b(){}
    void a(){}
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected

def test_008():
    source = """
class test {
    void foo(int a) {
        int b;
        int a;
    }
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_009():
    source = """
class test {
    void foo(int a) {
        int b;
        final int a;
    }
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected

def test_010():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        int c;
    }
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Variable, c)"
    assert Checker(source).check_from_source() == expected

def test_011():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int a;
            int e, c, e;
        }
    }
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Variable, e)"
    assert Checker(source).check_from_source() == expected

def test_012():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int c;
            final int c;
        }
    }
}
class votien{static void main(){}}
"""
    expected = "Redeclared(Constant, c)"
    assert Checker(source).check_from_source() == expected

def test_013():
    source = """
class votien{
    void main(){}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_014():
    source = """
class votien1{
    static void main(int a){}
}
class votie2{
    static void main(){}
}
class votien3{
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_015():
    source = """
class A extends io {}
class B extends A {}
class C extends Z {}

class votien{static void main(){}}
"""
    expected = "UndeclaredClass(Z)"
    assert Checker(source).check_from_source() == expected

def test_016():
    source = """
class votien{static void main(){
    int a := 1;
    a := b;
}}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected

def test_017():
    source = """
class votien{
    int a;

    static void main(){a:= 1;}
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_018():
    source = """
class votien{
    int a;
    int b := a;
    static void main(){}
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_019():
    source = """
class votien{
    int a;
    static void main(){
        this.a := 1;
        this.b := 1;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_020():
    source = """
class votien{
    int foo(){return 1;} 
    static void main(){
        int a;
        a := this.foo();
        a := this.coo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_021():
    source = """
class A {int foo(){return 1;}}
class votien{
    A a;
    static void main(){
        int a;
        a := this.a.foo();
        a := this.a.coo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_022():
    source = """
class votien{
    void foo(){}
    static void main(){
        this.foo();
        this.coo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_023():
    source = """
class votien{
    static void main(){
        final int a := 1;
        int  b;
        {
            b := a;
            a := b;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_024():
    source = """
class votien{
    final int a := 1;
    votien(){}
    static void main(){this.a := 2;}
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_025():
    source = """
class votien{
    static void main(){
        final int i := 1, j;
    }
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected

def test_026():
    source = """
class votien{
    static void main(){
        final int i := 1;
        final int j := 1 + i;
        final float k := (+i * -j) / 2;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_027():
    source = """
class votien{
    static void main(){
    final int MAX_SIZE := 100;
    final int DOUBLE_SIZE := MAX_SIZE * 2;     # Valid: uses immutable attribute
    final string MESSAGE := "Hello" ^ "World"; # Valid: literal concatenation
    final boolean FLAG := true && false;       # Valid: boolean literals with operators
    final float PI := 3.14159;
    final float CIRCLE_AREA := PI * 10 * 10;   # Valid: uses final attribute

    final int SUM := 10 + 20 + 30;         # Valid: literal arithmetic

    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_028():
    source = """
class votien{
    final int MAX_SIZE;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected

def test_029():
    source = """
class votien{
    final int MAX_SIZE := 1;
    final int A := this.MAX_SIZE;
    final int b :=  this.A * this.MAX_SIZE;
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_030():
    source = """
class votien{
    int MAX_SIZE := 1;
    final int A := this.MAX_SIZE;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).MAX_SIZE))"
    assert Checker(source).check_from_source() == expected

def test_031():
    source = """
class votien{
    static void main(){
          boolean[2] mixed3 := {true, 1};  
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected

def test_032():
    source = """
class votien{
    static void main(){
        int a; boolean b; float c; string d;
        a := 1;
        b := true;
        c := 1.0;
        c := 1;
        d := "s";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_033():
    source = """
class votien{
    static void main(){
        int[2] a;
        a := {1,2};
        a := {1, 2, 3};
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)})))"
    assert Checker(source).check_from_source() == expected

def test_034():
    source = """
class votien{
    static void main(){
        float[2] a;
        a := {1.0,2.0};
        a := {1,2};
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := ArrayLiteral({IntLiteral(1), IntLiteral(2)})))"
    assert Checker(source).check_from_source() == expected

def test_035():
    source = """
class A {}
class B extends A {}
class C extends B {}

class votien{
    static void main(){
        A a; B b; C c;
        c := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_036():
    source = """
class A {}
class B extends A {}
class C extends A {}

class votien{
    static void main(){
        A a; B b; C c;
        a := b;
        a := c;
        b := c;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := Identifier(c)))"
    assert Checker(source).check_from_source() == expected

def test_037():
    source = """
class A {}
class B extends A {}

class votien{
    static void main(){
        A[2] a; B[2] b;
        a := a;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_038():
    source = """
class votien{
    static void main(){
        int a;
        if a then {}
    }
}
"""
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(a) then BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_039():
    source = """
class votien{
    static void main(){
        int i; float f;
        for i := 0 to f do { }
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to Identifier(f) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_040():
    source = """
class votien{
    static float foo(){return 1;}
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_041():
    source = """
class votien{
    void foo(){}
    int coo(){return 1;}
    static void main(){
        this.foo();
        this.coo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_042():
    source = """
class votien{
    void foo(float a){}
    static void main(){
        this.foo(1.0, 1);
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_043():
    source = """
class votien{
    static void main(){
        int[2] a;
        int b;
        b := a[b];
        b := a[1.0];
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(a)[FloatLiteral(1.0)]))"
    assert Checker(source).check_from_source() == expected

def test_044():
    source = """
class votien{
    static void main(){
        int[2] a;
        string b;
        b := b[1];
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(b)[IntLiteral(1)]))"
    assert Checker(source).check_from_source() == expected

def test_045():
    source = """
class A {int[2] a; int[2] foo() {return this.a;}}
class votien{
    A a;
    static void main(){
        this.a.a[1] := this.a.a[1];
        this.a.a[1] := this.a.foo()[1];
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_046():
    source = """
class votien{
    static void main(){
        int[2] a;
        string b;
        a[b] := 1;
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(a)[Identifier(b)]))"
    assert Checker(source).check_from_source() == expected

def test_047():
    source = """
class votien{
    static void main(){
        int[2] a;
        string b;
        b[1] := 1;
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(b)[IntLiteral(1)]))"
    assert Checker(source).check_from_source() == expected

def test_048():
    source = """
class A { int i;}
class B {A a; A fa(){return this.a;}}
class votien{
    B b;

    static void main(){
        int a;
        a := this.b.a.i;
        a := this.b.a.i.i;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_049():
    source = """
class votien{
    static void main(){
        int a;
        a.b := 1;
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(a).b))"
    assert Checker(source).check_from_source() == expected

def test_050():
    source = """
class votien{
    void foo(){}
    static void main(){
        int a;
        a := this.foo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_051():
    source = """
class votien{
    int foo(float a){return 1;}
    static void main(){
        int a;
        a := this.foo(1);
        a := this.foo(1.0);
        a := this.foo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_052():
    source = """
class B{}
class A extends B{
    A(){}
    A(int a){}
    A(float a; string b){}
}
class votien{
    static void main(){
        A a; B b;
        a := new A();
        b := new A(1);
        b := new A(1, "S");

    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_053():
    source = """
class B{}
class A extends B{
    A(){}
    A(int a){}
    A(int a; string b){}
}
class votien{
    static void main(){
        A a; B b;
        a := new A(1.2);
    }
}
"""
    expected = "TypeMismatchInExpression(ObjectCreation(new A(FloatLiteral(1.2))))"
    assert Checker(source).check_from_source() == expected

def test_054():
    source = """
class votien{
    int foo() {
        int a;
        return 1 % a;
        return a \\ 3;
        return 1.2 % 2;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(FloatLiteral(1.2), %, IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_055():
    source = """
class votien{
    boolean foo() {
        return 1 != 2;
        return true == false;
        return 1 != true;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), !=, BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected

def test_056():
    source = """
class votien{
    boolean foo() {
        return 1.2 == 1;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(FloatLiteral(1.2), ==, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_057():
    source = """
class votien{
    boolean foo() {
        return 1.2 == 1.0;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(FloatLiteral(1.2), ==, FloatLiteral(1.0)))"
    assert Checker(source).check_from_source() == expected

def test_058():
    source = """
class votien{
    boolean foo() {
        return 1.2 > 1.0;
        return 1.2 >= 1;
        return 1 < 1.0;
        return 1 <= 1;
    }
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_059():
    source = """
class votien{
    static void main(){
        int x := 10, y := 20;
        int & xRef := x;
        int & yRef := y;
        xRef := x;
        x := yRef;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_060():
    source = """
class votien{
    static void main(){
        int x := "s";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('s'))]))"
    assert Checker(source).check_from_source() == expected

def test_061():
    source = """
class votien{
    final int x := "s";
    static void main(){
        
    }
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(x = StringLiteral('s'))]))"
    assert Checker(source).check_from_source() == expected

def test_062():
    source = """
class votien{
    static void main(){
        final int x := "s";
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(int), [Variable(x = StringLiteral('s'))]))"
    assert Checker(source).check_from_source() == expected

def test_063():
    source = """
class A {void coo() {} static void foo() {}}
class votien{
    A a;
    static void main(){
        this.a.coo();
        this.a.foo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_064():
    source = """
class A {int coo() {return 1;} static int foo() {return 1;}}
class votien{
    A a;
    static void main(){
        int x := A.foo() + A.coo();
    }
}
"""
    expected = "IllegalMemberAccess(.coo())"
    assert Checker(source).check_from_source() == expected

def test_065():
    source = """
class A {static int a; int b;}
class votien{
    A a;
    static void main(){
        A.a := 1;
        A.b := 2;
    }
}
"""
    expected = "IllegalMemberAccess(.b)"
    assert Checker(source).check_from_source() == expected

def test_066():
    source = """
class Example1 {
    int factorial(int n){
        if n == 0 then return 1; else return n * this.factorial(n - 1);
    }

    static void main(){
        int x;
        x := io.readInt();
        io.writeIntLn(this.factorial(x));
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_067():
    source = """
class votienB{
    final int[2] b := {1,2};
    static void main(){
        this.b[1] := 1;
        this.b := {3, 4};
    }

}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_068():
    source = """
class A {}
class votien{
    A a := nil;
    static void main(){
        A& b := this.a;
        A& c := b;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_069():
    source = """
class votien{
    static void main(){
        A.a := 1;
    }
}
class A {static int a := 1;}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_070():
    source = """
class votien extends votien{
    static void main(){
    }
}
"""
    expected = "UndeclaredClass(votien)"
    assert Checker(source).check_from_source() == expected

def test_071():
    source = """
class A {}
class votien{
    static void main(){
        A a;
        B b;
    }
}
"""
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected

def test_072():
    source = """
class A {}
class votien{
    A a;
    B b;
    static void main(){}
}
"""
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected

def test_073():
    source = """
class Animal {
    void makeSound() {
        io.writeStrLn("Some sound");
    }
}
class Dog extends Animal {
    void makeSound() {
        io.writeStrLn("Woof!");
    }
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_074():
    source = """
class Car {
    string brand;
    int year;

    void display() {
        io.writeStrLn(this.model);
    }
}
"""
    expected = "UndeclaredAttribute(model)"
    assert Checker(source).check_from_source() == expected

def test_075():
    source = """
class MathUtils {
    static int factorial(int n) {
        if n <= 1 then return 1; else return n * this.factorial(n - 1);
    }
}

"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_076():
    source = """
class Animal {
    string species;

    void setSpecies(string s) {
        this.species := s;
    }
        static void main(){}
}

class Dog extends Animal {
    void identify() {
        this.setSpecies("Canine");
        io.writeStrLn(this.species);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_077():
    source = """
class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        int[2] smallArray := {1, 2};

        intArray := smallArray;
    }
}

"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(smallArray)))"
    assert Checker(source).check_from_source() == expected

def test_078():
    source = """
class Shape {}

class Integer {}

class ObjectConstantError {
    final Shape shape1 := new Shape();
    final Shape shape := new Integer();
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer()))]))"
    assert Checker(source).check_from_source() == expected

def test_079():
    source = """
class LoopError {
    void conditionalError() {
        if true then {
            break;
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_080():
    source = """
class ValidLoops {
    void forLoopWithBreak() {
        int i, j;
        for i := 0 to 10 do {
            if i == 5 then {
                break;
            }
            if i % 2 == 0 then {
                continue;
            }
            io.writeIntLn(i);
        }
    }

    void forLoop() {
        int i, j;
        for i := 0 to 10 do {
            if i == 3 then {
                continue;
            }
            if i == 8 then {
                break;
            }
            io.writeIntLn(i);
        }
    }

    void nestedLoops() {
        int i, j;
        for i := 0 to 5 do {
            for j := 0 to 5 do {
                if i == j then {
                    continue;
                }
                if j > 3 then {
                    break;
                }
            }
        }
    }

    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_081():
    source = """
class IllegalConstantError {
    final string text := nil;
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected

def test_082():
    source = """
class Student {
    void resetCount(Student a; A b) {

    }
}
class A{}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_083():
    source = """
class IOTest {
    static void main() {
        int i := io.readInt();
        float f := io.readFloat();
        boolean b := io.readBool();
        string s := io.readStr();

        io.writeInt(i);
        io.writeIntLn(i);
        io.writeFloat(f);
        io.writeFloatLn(f);
        io.writeBool(b);
        io.writeBoolLn(b);
        io.writeStr(s);
        io.writeStrLn(s);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_084():
    source = """
class votien{
    static void main(){
        int a := 5;
        float b := a + 1.5;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_085():
    source = """
class votien{
    static void main(){
        string s := "Hello" ^ " " ^ "World";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_086():
    source = """
class votien{
    static void main(){
        boolean b := true || false && true;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_087():
        source = """
    class test {
        int a := 1;
        test() {}
        ~test() {}
        test(int a; int b) {}
    }
    class votien{static void main(){}}
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected

def test_088():
        source = """
    class votien extends votien{
        static void main(){
        }
    }
    """
        expected = "UndeclaredClass(votien)"
        assert Checker(source).check_from_source() == expected

def test_089():
    source = """
class votien{
    static void main(){
        int a := 10;
        int b := -a;
        int c := +a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_090():
    source = """
class votien{
    static void main(){
        boolean a := true;
        boolean b := !a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_091():
    source = """
class votien{
    static void main(){
        int a := 5;
        if a > 3 then {
            io.writeIntLn(a);
        } else {
            io.writeIntLn(0);
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_092():
        source = """
    class Animal {
        string species;
    
        void setSpecies(string s) {
            this.species := s;
        }
            static void main(){}
    }
    
    class Dog extends Animal {
        void identify() {
            this.setSpecies("Canine");
            io.writeStrLn(this.species);
        }
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected

def test_093():
    source = """
class A {
    static int count := 0;
    static void increment() {
        A.count := A.count + 1;
    }
}
class votien{
    static void main(){
        A.increment();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_094():
    source = """
class votien{
    static void main(){
        int a;
        continue;
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_095():
    source = """
class votien{
    void test(){
        int a;
        continue;
    }
    static void main(){}
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_096():
    source = """
class A {
    int x, y, x;
}
class votien{
    static void main(){}
}
"""
    expected = "Redeclared(Attribute, x)"
    assert Checker(source).check_from_source() == expected

def test_097():
    source = """
class A extends B {}
class votien{
    static void main(){}
}
"""
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected

def test_098():
    source = """
class votien{
    int foo(int a; int b){
        return a + b;
    }
    static void main(){
        int x := this.foo(1, 2, 3);
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_099():
    source = """
class votien{
    static void main(){
        int a := 10;
        float b := 5.5;
        string c := a ^ b;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), ^, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_100():
    source = """
class Parent {
    int value := 10;
}
class Child extends Parent {
    void display() {
        io.writeIntLn(this.value);
    }
}
class votien{
    static void main(){
        Child c := new Child();
        c.display();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


