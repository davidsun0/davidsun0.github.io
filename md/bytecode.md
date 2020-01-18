# Compiling for the Java Virtual Machine

## Overview

The JVM is a bytecode virtual machine.

Similar to assembly, but simpler.

Local variables and the stack

## Class File Format

```
CA FE BA BE     java magic number
00 00 00 37     java version 55.0 (java 11)
XX XX           constant pool length + 1

constant pool

00 21           extendable (not final) and public
XX XX           pool index of class name (classref)
00 00           implements zero interfaces
00 00           zero class fields
XX XX           number of methods

methods

00 00           zero attributes
```

## Constant Pool Table

## Method Format

```
00 09           public static
XX XX           pool index of function name
XX XX           pool index of function signature
00 01           attribute size of 1: code attribute
XX XX           pool index of "Code" (utf8)
XX XX XX XX     size of function
XX XX           maximum stack size
XX XX           maximum number of locals used

source bytecode (length in bytes is code size)

00 00       zero exceptions

stack map table 
```

## Stack Map Table and Frames


## Additional notes

## Method Names

`<clinit>` is reserved for the static initializer. It must be `static void` and
take no arguments.

A method may not have any of `<`, `>`, or `;` in its name.
