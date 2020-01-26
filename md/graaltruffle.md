# Creating a Language with Graal + Truffle

## Resources Used

### One VM to Rule Them All (Talk by Oracle)
Introduction to Truffle and basic tutorial on its usage with SimpleLanguage

- [One VM to Rule Them All, One VM to Bind Them](https://www.youtube.com/watch?v=FJY96_6Y3a4)
- [One VM to Rule Them All Slides [PDF]](https://lafo.ssw.uni-linz.ac.at/pub/papers/2016_PLDI_Truffle.pdf)
- [SimpleLanguage Github](https://github.com/graalvm/simplelanguage)
- [My Notes on SimpleLanguage](simple.html)


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
talk. The talk is focused on [SimpleLanguage](simple.html), which was created to
demonstrate Truffle's features.

## Implementing Conditionals: SLIfNode

All AST Nodes inherit from `com.oracle.truffle.api.nodes.Node`
- `Node` provides basic AST manipulation functionality (get parent, get children)

Example: implementing an if node

Source code: `com.oracle.truffle.sl.nodes.controlflow.SLIfNode`

### The Manual Way

The node has three children: one expression node and two statement nodes.
The expression node is evaluated first, and then one of the two statement nodes will
be evaluated after that.

- Create three fields in the `SLIfNode` class, one for each child
- Annotate each child with `@Child`
- Write a SLIfNode constructor to set the three children
- Implement logic in `ifNode.executeVoid(VirtualFrame)`

```
public final class SLIfNode extends SLStatementNode {
    @Child private SLExpressionNode conditionNode;
    @Child private SLStatementNode thenNode;
    @Child private SLStatementNode elseNode;
    ...
}
```

### With Truffle Annotations

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
}
```

### Increasing perfomance via profiling

Implement branch prediction with `com.oracle.truffle.api.profiles.ConditionProfile`:

- create an instance with `ConditionProfile.createCountingProfile()` in the objects'
initializer
- wrap evaluation of the condition node in `conditionProfile.profile()`

## AST Node Optimization: Specializations

Specializations can increase language performance. For SimpleLanguage, even though it
has arbitrary precision integers, in practice programs are much more likely to be working
with small numbers. It would be a waste to use Java's BigInteger for all calculations.

Truffle allows SimpleLanguage's integers to be backed by long or BigInteger and it can
automatically convert as needed. For this, we will need:
- A function detailing the implicit conversion in the type system (`SLTypes`)
- Special functions in arithmetic nodes which can handle long and BigInteger

For the addition node, we first implement the logic for adding two long values.
To upcast to BigInteger when necessary, we use `Math.addExact`, which will throw
and ArithmeticException error when the addition overflows.

```
@NodeChildren({@NodeChild("leftNode"), @NodeChild("rightNode")})
public class SLAddNode extends SLExpressionNode {
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

When the addition with longs fails with an ArithmeticException, the next specialization
will be attempted. If that specialization has a rewrite, Truffle will then continue
down the list of specializations (in the order of the source code).

Furthermore, the addition operator can be overloaded to take strings. In SimpleLanguage,
addition with strings performs concatenation. To avoid concatenating two integers,
we use the type system and gaurds to check the types of the arguments. (Note that in
SimpleLanguage, integers cannot be automatically cast to strings).

To implement string concatenation with the + operator, simply write a specialization that takes
Strings as arguments. The gaurd and isString function checks to see that at least one
of the arguments is of type String.

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

//TODO 1:21:00
