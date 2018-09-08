=======
Wooble
=======

Welcome to Wooble! Wooble is my attempt at writing an interpreter and learning in the process.
I gladly welcome feedback and hope to learn from it.

The Name
---------

See this Blackadder `sketch <https://youtu.be/G2DCExerOsA>`_.

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

Data Types
-----------

Wooble currently supports strings and floats. More data types will be added as needed/desired.

Syntax
-------

As was mentioned, Wooble is a lisp. Currently the list of reserved keywords/symbols is as follows:

def
    Creates a variable called SYMBOL with value BODY.
    Usage::

        (def SYMBOL BODY)

*
    Cumulative multiplication. This is normal multiplication if you only have
    2 numbers. With more than 2, the multiplication accumulates using a reduce
    type of operation. Usage::

        (* NUMBER+)

Hacking on Wooble
------------------




