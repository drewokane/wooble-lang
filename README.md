Wooble
=======

Welcome to Wooble! Wooble is my attempt at writing an interpreter and learning in the process.
I gladly welcome feedback and hope to learn from it.

The Name
---------

See this Blackadder [sketch](https://youtu.be/G2DCExerOsA).

The Language
-------------

Wooble is an interpreted lisp. The current features include all the basic arithmetic operations
and variable assignment. In all honesty, Wooble is a glorified lisp calculator. But what a
calculator!

If you've dealt with lisp-like languages before you should have no problem writing a script in
Wooble. For those of you who've never encountered a lisp before, essentially operators are prefix
not infix like "normal" mathematics we write. So a mathematical operation like:

    2 + 3

...becomes:

    (+ 2 3)

You'll get used to it. Very smart people who practice functional programming will tell you this
comes from lambda calculus.

Hacking on Wooble
------------------

The Wooble interpreter is written in Python with the help of [lark](https://github.com/lark-parser/lark). The
project is set up using [poetry](https://poetry.eustace.io/). You'll need to install `poetry` to
get the project working properly of course but beyond this it should be a 
breeze to get started with Wooble.

For more info, check out the [wiki](https://github.com/drewokane/wooble/wiki).
