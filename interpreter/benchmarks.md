# BFASM Interpreter Benchmarks
The following is some benchmarks from different versions of the BF-ASM interpreter. Each benchmark was performed with the ```time``` unix utility.

## Interpreter 0.1.0
0.1.0 was a basic implementation of a BF interpreter. It had no optimizations and seems to fail to run any complicated programs.

| Program         | Result        |
| --------------- | ------------- |
| *mandelbrot.bf* | Failed        |
| *hello.bf*      | 0.009 seconds |
| *99bottles.bf*  | Failed        |
| *sierpinski.bf* | Failed        |

## Interpreter 0.1.1
0.1.1 introduced a precalculated jump table. 0.1.0 calulcated where to jump on the fly, but 0.1.1 pre-calculated these jumps. Every function in the interpreter was inlined as well, since each function was only used once and only existed as a function for organizational purposes.

| Program         | Result          |
| --------------- | --------------- |
| *mandelbrot.bf* | 2:28.29 minutes |
| *hello.bf*      | 0.0075 seconds  |
| *99bottles.bf*  | 0.019 seconds   |
| *sierpinski.bf* | 0.010 seconds   |