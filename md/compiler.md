# Implementing Tail Call Optimization

## Benefits of tail recursion
Lateral Lisp has no for or while loops. For Lateral, it is often more natural
to express looping with recursion. This is because Lateral Lisp does not
have variables like in C or Java. Functions only pass values and these values
can't be changed.
(This isn't true for all Lisps, or even most Lisps, but it
makes writing a Lateral compiler much simpler.)

However, recursion can be expensive. Every time a new recursive call is made,
a new stack frame needs to be allocated. A recursive function that calls itself
too many times can cause a stack overflow and crash. In fact, this happened
quite often in the early stages of Lateral's development.

Tail call optimization allows a recursive call in the tail position to be
implemented as a GOTO to the beginning of the function. No new frame needs to
be allocated, and there are also perfomance benefits as well.

In fact, you could consider tail call optimization a compiler optimization which
converts tail recursive functions into while loops.

## What is the tail position?

Is a recursive call in the tail position? If the function returns the result of
the call without any further processing, the function is in the tail position.

```
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

The classic implementation of the factorial function would not be tail recursive.
After the recursive call is done, it still needs to be multiplied by n.

```
int factorial(int n, int total) {
    if (n <= 1) {
        return total;
    } else {
        return factorial(n - 1, total * n);
    }
}

int factorial(int n) {
    return factorial(n, 1);
}
```

The above function is tail recursive, and is more or less a direct translation
of the equivalent Lisp code. This may not seem like a big change, and in fact may
seem less intuitive. However, when all you have is a hammer everything looks like
a nail and Lateral's hammer is recursion.

In this form, the compiler can transform the factorial code into something like this:

```
int factorial(int n, int total) {
    while (n > 1) {
        total = total * n;
        n = n - 1;
    }
    return total;
}
```

Tada! The recursion has been optimized away!

To be specific, this isn't exactly what happens. Notice how the behavior of factorial
changes depending on whether `n = n-1` or `total = total * n` comes first. The generated
bytecode assigns both values _simultaneously_ to preserve the output of the original
code.

## Generating bytecode

Java has local variables as well as variables on the function's stack. Lateral
operates almost exclusively on the stack.

The first n local variables are set to the arguments of the function when it is
called. Therefore, if we replace those variables and jump to the start of the
function, it will be like the function was just called with those new variables.

Plan of action:
- Store the n variables currently on the stack into the local variables.
- Be sure that the stack is empty (that's the way the function was when it was
first called!)
- Jump to the beginning of the function

Storing the variables on the stack should be done in reverse order. The JVM's
calling convention is to have the last argument on the top of the stack.

```
[C] <-top
[B]
[A]
```
if function f is called right now with three arguments, it will be equivalent to
`f(A, B, C)`. We know the number of arguments the function has, so we can count
down to zero.

```
store_local 2
store_local 1
store_local 0
goto start
```

Start must be bytecode offset 0, and JVM's goto uses relative offsets, so the
offset is simply the negation of the current byte offset. If the goto happens
100 bytes into the function, the offset is -100.

The JVM requires stack information at all jump targets, so the compiler must
insert a frame indicating that there are 0 items on the stack at the beginning
of the function. The JVM will verify it, so if the compiler miscalculates the
number of objects on the stack, the program won't run.

