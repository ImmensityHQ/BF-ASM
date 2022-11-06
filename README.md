# BF-ASM

Assembly-like language that is assembled to brain*ck.

## What is it?

BF-ASM will be an easy to use, easy to read assembly-like language that will be almost like a text representation of brainf*ck, with some higher level features so it isn't a complete pain to use.

## How can I use it?

Right now BF-ASM is not usable and __WIP__.
Feel free to look around the code and contribute any changes.

## Feature Checklist

* Lexical analysis
  * [x] Scanning
  * [x] Tokenizing
  * [x] Yielding tokens
  * [x] (Some) errors
* Parser (Recursive descent)
  * [x] AST Definition (Partially completed, current syntax is super incomplete)
  * [x] Parsing
  * [x] (Some) Errors
* Codegen
  * [x] Basic codegen
  * [ ] Programmatically controllable interpreter class in Python
  * [ ] Generate code from AST

* Rust Interpreter
  * [x] Basic functionality
  * [x] Pre-calculated jump tables
  * [ ] Repeated operations optimizations

And finally, arguably most important of all:

* [ ] an actual syntax

I have ideas for what I *want* BF-ASM to do, but no idea for what the syntax would look like. I'm still laying the groundwork right now and will focus on syntax later.
