.source Main.java
.class public Main
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
Label2:
.var 1 is count I from Label2 to Label3
	iconst_0
	istore_1
.var 2 is i I from Label2 to Label3
	iconst_1
	istore_2
Label6:
	iload_2
	bipush 10
	if_icmpgt Label5
Label7:
	iload_2
	iconst_3
	irem
	iconst_0
	if_icmpne Label11
	iconst_1
	goto Label12
Label11:
	iconst_0
Label12:
	ifle Label9
Label13:
	iload_1
	iconst_1
	iadd
	istore_1
Label14:
Label9:
Label8:
Label4:
	iload_2
	iconst_1
	iadd
	istore_2
	goto Label6
Label5:
	iload_1
	invokestatic io/writeInt(I)V
Label3:
	return
Label1:
.limit stack 7
.limit locals 3
.end method

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
.limit stack 1
.limit locals 1
.end method
