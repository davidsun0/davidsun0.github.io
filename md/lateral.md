# Lateral Lisp

## Code Samples

### Hello World

### Factorial

### Fibonacci

### JVM Interop

# Differences from existing Lisps

## Better than Clojure

- Invokedynamic
- Access to JVM bytecode
- Better error messages than Clojure (eventually)
- Aggressively compatible with existing JVM code

## Better than (Armed Bear) Common Lisp

- Simple and easy to learn
- Simple to deploy
- Better names for functions

### Better names

I know how many programmers I'm going to annoy with this, but I seriously don't
like Common Lisp's names.

I don't care how much you like car / cdr. I think it makes a simple concept
unecessarily hard for newcommers. When I first started using Lisp, I constatnly
had to look up car, cdr, and cons. Programmers are used to working with lists
and sequences in other languages. Even for non-programmers, isn't it clearer to
say first, rest, and prepend?

Much less debated are things like lambda and progn, but I think those can be
made easier to learn too. I like how Clojure calls progn do. In Lateral, labmda
is function. Or maybe func. I haven't decided.

## Things Lateral is worse than existing Lisps at

Debugging in Common Lisp is sheer magic and it won't be easy to recreate that on
the JVM.
