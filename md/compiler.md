# Compiling Tail Recursive Functions

## Benefits of tail recursion
Lateral Lisp has no for or while loops. For Lisps, it is often more natural
to express looping with recursion.

Implementing recursion in the style of a language like C can be inefficient
because an additional call frame needs to be added to the stack for every
recurisve call.

Tail call optimization allows a recursive call in the tail position to be
implemented as a GOTO to the beginning of the function. No new frame needs to
be allocated.

In fact, from a bytecode or assembly point of view, tail optimized recursion is
identical to a while loop. If the base case is reached, the loop breaks.
Otherwise, the code is repeated with new arguments.

## What is the tail position?

Is a recursive call in the tail position? If the function returns the result of
the call without any further processing, the function is in the tail position.

In Lateral, functions can only have one function call in the body. This call
must be in the tail position.

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

