# Admin Service

## Solver

Ref: [Solver](./solve.py)

Notes:

* There is an off by one in `readInput` function. The call tree `main -> readDescription -> readInput` would result in overwriting a nullbyte in the least significant byte of the saved RBP in `readDescription` call-stack. The `leave; ret` instruction at the end of the `readDescription` would result in restoring the saved RBP after being modified. Chained with the `leave; ret` instruction at the end of the `main` function, this would result in a stack pivot.
* Send a large enough payload with a new line (which will be overwritten with a null byte). The payload should contain a ROP chain.
* This won't be always successful, the solve I provided calls `readInput` to write a stage 2 rop chain in bss then stack pivots.
