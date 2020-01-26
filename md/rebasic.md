# My First "Assembler": ReBasic

I was just looking through my old code and found [ReBasic](#).

It's an IDE + Assembler for the TI-83 and 84 series graphing calculators.
On the graphing calculators, you can write your own programs in a language
unofficially called TI BASIC (because it looks a lot like BASIC). The project
is written with Processing. The language is ultimately Java, but Processing
provides lots of libraries and does some preprocessing to make it beginner-friendly.

Back in
high school when I wrote this, I spent absurd amounts of time making little games
and other cool toys on it. My fondest memory is finding out that the function
that integrates the normal distribution is only accurate to 8 decimal places (if
I remember correctly), but it displays 10. We were learning about Taylor Series
in calculus class, and I was simultaneously taking statistics, so I wrote a program
to integrate the normal distribution, but the last two decimals were always different.
It turns out that my program was correct, and the calculator was wrong!
Well, I shouldn't give myself that much credit. The calculator's function was almost
instantaneous while my program took 10 seconds to run.

Anyways, ReBasic was a way for me to write programs on my computer and then transfer
them over the USB connector. The calculator didn't have a proper keyboard and all
commands had to be entered by hand.

Looking through the code, it seems like the TI BASIC programs all had a very simple format.
There is a header that's about 10 bytes long, and every token (command, variable,
symbol, etc) maps to one or two bytes in the program file. Even still, I'm very
impressed that it's written by a high school student.

Unfortunately it doesn't run
right out of the box. First of all, Processing expects the folder to match the name
of the main file. Since the entry point of the program is in rebasic.pde, the project
file needs to be renamed to rebasic.
ReBasic might not even work on modern versions of Processing, as
the code still relies on Java's AWT, which has been deprecated in later versions.
I'm currently using 3.3.5 on Linux, and there are other issues. I had to tweak file
loading to use Linux's forward slash instead of Windows backslash to save files.
(Although the README does say that it's only been tested on Windows...)
Additionally, assembling the output is completely broken. All of the coding logic
is there, but it isn't wired up correctly. I'm convinced that it did work at one
point in time though. I just don't see myself adding all of the other bells and whistles
if the core feature of ReBasic didn't work.

There's a lot of detail in the program. Processing only provides a 2D canvas, but
there's code to render all of the tokens onto the string. Special care is taken
to render mathematical symbols. There's even a dark theme! There isn't a way to change
it with the GUI, but changing [line 11 of rebasic.pde](#) to `colorscheme = night`
turns the program from light to dark!

In total, there are about 2000 lines of code, including whitespace and comments.
The code quality is actually higher than I expected. Nothing is awful in the moment
to moment code, but the overall architecture is... interesting. Still, 2000 lines is
pretty ambitious for a self taught high school student and it's impressive that it
more or less works. I wonder if I gave up because it simply became too hard to add
new features and make changes.

I like Me From the Past's willingness to write a text editor more or less from scratch.
All of the keystrokes are captured and there's logic for moving the cursor around
the screen. The text area even lets you scroll (manually with the arrow keys) beyond
the edge of the screen if your program becomes long!

Writing a text editor from scratch is
a nice solution to an interesting problem: on the calculator, typing out the letters
's', 'i', and 'n' doesn't give you the sin function. The letters and the commands are
seperate. The solution I came up with was inspired by Chinese keyboard inputs: you type
a series of letters and then press space. If the sequence of letters is a command,
ReBasic will automatically convert them into a single token. Press enter and the text you're
typing will be entered as literal characters. The working group of characters is underlined
for your programming convinence. Furthermore, tokens are colored so you can be sure
what your program represents. This is especially convinient for common symbols which
don't appear on the keyboard like the assignment operator, which is the right arrow.

This also solves the problem of many tokens
being hard to type on a keyboard. For example, typing 'arctan(' and pressing space creates the
'tan<sup>-1</sup>(' token. This works for every token. [There's a table.](#)

I'm surprised that I even took the time to draw images for glyphs that aren't in Unicode.
In data/glyphs, there are a few interesting symbols that must be unique to the TI-83.
You can type these glyphs with 'invertedequal', 'biguparrow', 'bigdownarrow',
'squaremark', '+mark', '.mark', and 'angle'.
