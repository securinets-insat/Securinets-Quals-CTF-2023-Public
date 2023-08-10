# Ret2libc

## Solver

Ref: [Solver](./solve.py)

Notes:

* Sending exactly 80 bytes + new line(which gets will replace with a null byte) will result in a null byte written in the least significant byte of the saved ECX value on stack.
* Include a rop chain in the 80 bytes. To increase success rate, use a ret slide with a short rop chain.
* You have a chance for the stack pivoting at the end of the `main` function to land on your payload & you execute a ROP chain.
