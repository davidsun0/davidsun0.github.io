# Creating a Language with Graal + Truffle

## Resources Used

### One VM to Rule Them All (Talk by Oracle)
Introduction to Truffle and basic tutorial on its usage with Simple Language

- [One VM to Rule Them All, One VM to Bind Them](https://www.youtube.com/watch?v=FJY96_6Y3a4)
- [One VM to Rule Them All Slides (PDF)](https://lafo.ssw.uni-linz.ac.at/pub/papers/2016_PLDI_Truffle.pdf)

### Language Implementations in Truffle

- [Mumbler Blog Posts](http://cesquivias.github.io/tags/truffle.html)
- [Mumbler (Github)](https://github.com/cesquivias/mumbler)
- [TruffleClojure](https://epub.jku.at/obvulihs/content/pageview/508383)
- [Truffle/C (PDF)](http://ssw.jku.at/General/Staff/ManuelRigger/thesis.pdf)

Mumbler is a simple dialect of Lisp made to demonstrate Truffle's features.

### Other Reading

- [Graal & Truffle](https://blog.plan99.net/graal-truffle-134d8f28fb69)
- [Top 10 Things to do with GraalVM](https://medium.com/graalvm/graalvm-ten-things-12d9111f307d)

### Reference

- [Truffle Javadoc](https://www.graalvm.org/truffle/javadoc/)

# Truffle Notes

These notes are mainly based on the [One VM to Rule Them All, One VM to Bind Them](https://www.youtube.com/watch?v=FJY96_6Y3a4)
talk. The talk is focused on [Simple Language](simple.html), which was created to
demonstrate Truffle's features.

## Implementing Conditionals: SLIfNode

All AST Nodes inherit from `com.oracle.truffle.api.nodes.Node`
- `Node` provides basic AST manipulation functionality (get parent, get children)

Example: implementing an if node

Source code: `com.oracle.truffle.sl.nodes.controlflow.SLIfNode`

The node has three children: one expression node and two statement nodes.
The expression node is evaluated first, and then one of the two statement nodes will
be evaluated after that.

- Create three fields in the `SLIfNode` class, one for each child
- Annotate each child with `@Child`
- Write a constructor
- Implement logic in `ifNode.executeVoid(VirtualFrame)`

### Increasing perfomance via profiling

Implement branch prediction with `com.oracle.truffle.api.profiles.ConditionProfile`
by wrapping evaluation of the condition node in `conditionProfile.profile()`.

Initialize an instance with `ConditionProfile.createCountingProfile()`

Use Truffle's annotations to automatically generate this code: Annotate the class to provide
information about its children.

For example, `SLAddNode` performs addition on a left and right child.
```
@NodeChildren({@NodeChild("leftNode"), @NodeChild("rightNode")})
public class SLAddNode extends SLExpressionNode {

    @Specialization    
    long add(long left, long right) {
        return left + right;
    }

    ...
```

## AST Node Optimization: Specializations

Continuing from the previous section, specializations can be used to get performance
increases. SimpleLanguage has arbitrary precision integers (as in Java's BigInteger),
so this optimization will be performed if both arguments fit in a long.

However, we can use `Math.addExact()`, which throws an `ArithmeticException` if the addition
overflows. When the overflow occurs, we can retry with BigInteger arithmetic.

```
    ...

    @Specialization(rewriteOn = ArithmeticException.class)
    long add(long left, long right) {
        return Math.addExact(left, right);
    }

    @Specialization
    BigInteger add(BigInteger left, BigInteger, right) {
        return left.add(right);
    }

    ...
```

A specialization can rewrite on multiple exceptions. After rewriting because of an
exception, the next specialization can throw an exception and delegate to the next one.

Note: Specializations are attempted in order of the source code. In this example, the long
version is attempted before the BigInteger version. If multiple specializations are valid
for the given inputs, the first one will be performed.

Furthermore, there needs to be an implicit
conversion from long to BigInteger declared in the language's type system.
For SimpleLanguage, this is in `com.oracle.truffle.sl.SLTypes.java`.

To overload the add operator to work with Strings, simply write a specialization that takes
Strings as arguments. SimpleLanugage's add performs string concatenation if one of the
arguments is a String. To prevent integers from being concatenated as strings, write a type
gaurd.

```
    ...

    @Specialization(gaurds = "isString(left, right)")
    String add(Object left, Object right) {
        return "" + left + right;
    }

    static boolean isString(Object left, Object right) {
        return left instanceof String || right instanceof String;
    }
}
```

If no specializations match or if gaurds prevent any specializations match, Truffle will
automatically throw a type error.

## Implementing expressions: SLExpressionNode

- Can provide `executeLong`, `executeBoolean`, etc for performance speedups to avoid
interpreter type unboxing (e.g. Java's `bool` vs `Boolean`)

## Implementing code blocks: SLBlockNode

BlockNode contains a block of code and evaluates every child.

- Create a final array of SLStatementNode
- Annotate with `@Children`

```
@ExplodeLoop
@Override
public void executeVoid(VirtualFrame frame) {
    for (SLStatementNode bodyNode : bodyNodes) {
        bodyNode.executeVoid(frame);
    }
}
```

- `@ExplodeLoop` causes Truffle to unroll the loop instead of iterating over bodyNodes
- This is possible because bodyNodes is final, so the number of iterations is known

## Control through multiple execution frames

In SLReturnNode, throw a `SLReturnException`, and catch this exception in the function
AST node. Truffle removes the exception overhead.

## Local Variables and Frame Types

//TODO
