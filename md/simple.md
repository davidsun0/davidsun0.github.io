# SimpleLanguage

[Github](https://github.com/graalvm/simplelanguage)

[Getting Started](https://www.graalvm.org/docs/graalvm-as-a-platform/implement-language/)

[One VM To Rule Them All Slides (PDF)](https://lafo.ssw.uni-linz.ac.at/pub/papers/2016_PLDI_Truffle.pdf)

SimpleLanguage is a high-level, C-style, dynamically and strongly typed programming language.

SimpleLanguage is made by Oracle as a demonstration of their compiler framework, Truffle.
Because it is an example codebase for language creation, the code is well documented.

This page is a collection of my notes on how the language works and its implementation.


## Code Samples

### Hello World
```
function main() {
    println("Hello World!");
}
```

### String Manipulation
```
function f(a, b) {
    return a + " < " + b + ": " + (a < b);
}

function main() {
    println(f(2, 4))
    println(f(2, "4"))
}
```

### Objects
```
function main() {
    obj = new();
    obj.prop = "Hello World!";
    println(obj["pr" + "op"]);
}
```

### Looping
```
function main() {
    i = 0;
    sum = 0;
    while (i <= 10000) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
```

### Function Definition / Redefinition
```
function foo() {
    println(f(40, 2));
}

function main() {
    defineFunction("function f(a, b) { return a + b }");
    foo();

    defineFunction("function f(a, b) { return a - b }");
    foo();
}
```

### First Class Functions
```
function add(a, b) { return a + b; }
function sub(a, b) { return a - b; }

function foo(f) {
    println(f(40, 2));
}

function main() {
    foo(add);
    foo(sub);
}
```

## Features

SimpleLanguage has support for arbitrary precision integers.
