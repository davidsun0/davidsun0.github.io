# Invoke Dynamic: I can't come up with a good title

# Overview

- What is indy? (JVM, bytecode)
- Why indy?

# Why invoke dynamic?

As a faster version of Java's reflection.

JVM is statically typed: all types must be known at compile time.
indy makes the JVM slightly more dynamic.
Allows for limited runtime code generation.

# What invoke dynamic can't do

When I first heard about Invoke Dynamic, I had some misconceptions on what it
could be used for.

- multiple dispatch
- dynamic dispatch

As I understand it, these won't work because changing what method is being
bound is somewhat expensive performance wise.

# What invoke dynamic can do

This is how I'm using invoke dynamic in my JVM programming language, called
Lateral Lisp.

Generate constatns at runtime
call methods not present or known at compile time
"creating" new methods at runtime
- putting existing methods together, not actually code generation at runtime

Modify a method call

Doesn't even need to be a method
What's the difference of calling a void method that returns an object and
directly loading that object?

## Calling a method that doesn't exist yet

In order to be insanely malleable, Lateral compiles the file incrementally.
Function calls are not resolved at compile time. Not knowing a function at
compile time is not a problem. It is only an error when a program calls a
function that hasn't been defined.

When a function is actually called, the bootstrap method finds the method in the
user environment. With that, the function is "installed" and that's that.

### Changing what method is being called

I plan on using MutableCallSites in Lateral function calls. This way, I can
redefine a function. If the environment keeps track of every CallSite created,
I can simultaneously replace every call to a function at once.

The only thing I need to worry about is if the redefined function has the same
number of arguments as the old one... or do I?

### Modifying how a method is calld

Inserting constatn ojbects
preprocessing arguments
shuffling arguments
packing and unpacking arguments

Lateral variable argument functions put the extra functions in a Sequence data
structure.

```
Object callerFunction() {
   myFunction(1, "Hello", null);
}

Object myFunction(Object a, Object b, Object c) {
    ...
}

// redefine the function
Object myFunction(Object ... args) {
    ...
}
```

The varargs is processed by the Java compiler. It's the compiler's job to
generate code which packs the arguments. In Lateral, the caller can't tell
if the function its calling is varargs. In fact, I might redefine the function
and change if its varargs or not.

So when the bootstrap method calls myFunction, it has access to the function
and will check how to call it. Using `java.lang.invoke.MethodHandles`, I can
modify how the function is called.

I make a CallSite which first binds the varargs, then passes that result to the
original function. It hides all the complexity.

## Calling a method without knowing its types

This was the example I saw the most online. Something about JRuby.

## Generating constant objects at runtime

In Lateral, Symbols and Keywords are a key part of the language. To save on
some memory and computation time, they have to be created with a special
function. However, once they are generated, they are essentially constants
and can be reused and passed around at will.

Since making Symbols and Keywords can be expensive, we want to save the
created object. One option would be to make the objects in the class' static
initializer.

That's a lot of work and I don't feel like doing all of it.

The first time the invokedynamic is visited, the Symbol is generated. The
object is saved in the ??? CallSite, and every subsequent call, the existing
object is reused.

# Things I don't know

To be honest, I have no idea what I'm doing, and I think it's important that
you know.

I may have gotten things wrong. I'm just putting this out there so the next
person who needs invokedynamic in a non-professional setting won't spend weeks
wandering the internet.

- Can different objects have different bound methods?
- Are CallSites garbage collected if the Class with the invokedynamic
instruction is collected?

Thanks for reading. Peace.
