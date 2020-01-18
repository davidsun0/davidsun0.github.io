# Creating JVM Classes at Runtime

This is how Lateral Lisp compiles at runtime.

## Java Class Loaders

The java.lang.ClassLoader class can allow new classes to be loaded at runtime.
This can be used to load code from a network, or in Lateral's case, to compile
new user defined functions.

A relative to self-modifying code, this allows the JVM program to extend its
functionality while running.

## Class Generation

The bytes of a valid JVM class must be loaded into a byte array.

## Code

```
class MyClassLoader extends ClassLoader {
    public Class<?> defineClass(byte[] bytes) {
         return defineClass(null, bytes, 0, bytes.length);
    }
}
```

Reflection must be used to extract and call the methods of the generated class.

## Notes

A loaded class cannot call protected or private methods of a class in the same
package but loaded by another ClassLoader.

Classes keep a reference to their ClassLoader. When there are no more references
to the classes or the ClassLoader, they will be discarded by the garbage
collector.

## Sources

[https://www.baeldung.com/java-classloaders](https://www.baeldung.com/java-classloaders)
