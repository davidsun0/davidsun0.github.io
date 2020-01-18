# A new pass for lambdas
### November 23 2019

I'm working on compiling anonymous fuctions and am faced with a new problem.

First of all, while compiling one function, the compiler may have to compile
another function. And that function may have even more functions inside of it.
Since functions are a type of object, the compiler needs to compile a Lisp
lambda into a Java function and wrap it inside of an object.

It might be useful to add a new compiler pass. Each lambda will be left alone
and only marked with the token `:labmda` in the regular ast to ir step. Then
the new pass will filter out these lambdas. The lambdas will be compiled just
like any other function, and the slot in the ir will be replaced with a `:push
lambda-numberX` token.

At the same time, the lambda will be labeled with the same `lambda-numberX`
symbol. The lambda object will need to be made in the static initializer.

The new problem is that an anonymous function may be used as either a function
or as an object. If the first happens, then the compiler needs to generate code
to call the function object. The ast to ir step will have to generate the start
of a function call to distinguish the different uses.

```lisp
# original ast
(a b c d)

# current ir
(:push b)
(:push c)
(:push d)
(:funcall a :argc 3)

# new ir
(:call)
(:push a)
(:push b)
(:push c)
(:push d)
(:funcall :argc 4)
```

The downside to this approach is that there needs to be a pass to determine
if a variable should be looked up in the global environment or from the
function's arguments. The upside is that this will simplify calling functions
that were passed as arguments or created from a higher order function.

I still have no idea how to implement closures though. I'll probably have to
modify this solution if I want the anonymous functions to close over variables
in the outer scope.

Basically what I'm trying to say here is that the JVM makes it a pain to
implement first class functions.

# The Lambda-Closure Problem
### December 1 2019

For my first crack at this problem, I'll assume that all lambdas are closing
over some internal variable. This is the general case, and then I can work on
optimizations for things like calling a lambda immediately after its made.

If a lambda is closing over an internal variable, the lambda must be made at
runtime. The compiler should emit code to construct the lambda, not the lambda
itself.


