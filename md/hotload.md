# Creating JVM Classes at Runtime

This is how Lateral Lisp compiles new Lisp to Java Bytecode at runtime.

## Java Class Loaders

The `java.lang.ClassLoader` class can allow new classes to be loaded at runtime.
This can be used to load code from a network, or in Lateral's case, to compile
new user defined functions. This allows Lateral to be both fast and highly flexible
at the same time.

Class loading is like self-modifying code, but it has all of the safety features
that Java comes with.
With class loaders, a JVM program can extend its functionality while running.

## Class Generation

Compilation happens like usual. Lateral Lisp code is transformed into a Java
class file. However, instead of writing the file to disk, the byte array can be
immediately loaded into the running program.

## Code

```
class MyClassLoader extends ClassLoader {
    public Class<?> defineClass(byte[] bytes) {
         return defineClass(null, bytes, 0, bytes.length);
    }
}
```

The new class is then available to call from existing code. To get a handle on
the new functions, reflection is used to get the new class' methods and store
them in the environment.

## Notes

A loaded class cannot call protected or private methods of a class in the same
package but loaded by another ClassLoader.

Classes keep a reference to their `ClassLoader`. When there are no more references
to the classes or the ClassLoader, the ClassLoader and __the class itself__ will be
reclaimed by the garbage collector.

## Sources

[https://www.baeldung.com/java-classloaders](https://www.baeldung.com/java-classloaders)
