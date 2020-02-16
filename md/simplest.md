# SimplestLanguage: Getting Started with Truffle

SimplestLanguage is the bare minimum of code needed for a working
language on the Graal + Truffle platform. [SimpleLanguage](simple.html)
may be simple compared to mainstream programming languages, but it's
still quite complicated and requires a lot of reading to get familiar with.

Goal: make a language that can parse and print a number.

## Simplest POM

Using Maven will make it easier to manage dependencies for the project.
Of course, `<graalvm.version>` should be changed as needed.

IDEs like IntelliJ should automatically detect and download the appropriate files
with this `pom.xml` file. Be sure to change the groupId and artifactId
with the Java package and project name of the language approprately.

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>PROJECT PACKAGE</groupId>
    <artifactId>YOUR LANGUAGE NAME</artifactId>
    <version>1.0-SNAPSHOT</version>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <graalvm.version>19.3.0</graalvm.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.graalvm.truffle</groupId>
            <artifactId>truffle-api</artifactId>
            <version>${graalvm.version}</version>
        </dependency>
    </dependencies>
</project>
```

## Main

```
public static void main(String[] args)
```

Friend of CS 101 students everywhere.

Things to do:

### Source Code
Build a `org.graalvm.polyglot.Source` object from source code

[Source](https://www.graalvm.org/truffle/javadoc/org/graalvm/polyglot/Source.html)

```
// From file:
Source.newBuilder(languageID, new File(file)).build();

// As a repl:
Source.newBuilder(languageID, new InputStreamReader(System.in), "<stdin>").build();
```

### Evaluation Context
Create a `org.graalvm.polyglot.Context` object with `SLLanguage`

[Context](https://www.graalvm.org/truffle/javadoc/org/graalvm/polyglot/Context.html)


`context.eval(source)`

## SLLanguage

`extends TruffleLanguage<SLContext>`

(Replace with your language's context)

`@TruffleLanguage.Registration(id, name)`

Are id and name even necessary?

### Abstract Methods:
- createContext
- isObjectOfLanguage

Define source code parsing (don't have to use Antlr)
Parser returns AST of Nodes
```
@Override
protected CallTarget parse(ParsingRequest pr) {
    RootNode evalMain;
    return Truffle.getRuntime().createCallTarget(evalMain);
}
```

## SLContext

[Context](https://www.graalvm.org/truffle/javadoc/org/graalvm/polyglot/Context.html)
