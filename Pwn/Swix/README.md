# Swix

## Solver

### Official

Ref: [Solver](./solve.py)

Notes:

* Source code was given to help with debugging.

* Exploiting the dlresolve function to call system("sh")
* System has access to environment variables (PATH) therefore, calling system("sh") would work perfectly fine.
* Puts uses heap before printing a message therefore, by leaking a heap address, you can calc the address of "I'm safe! I wish" stored in heap & should be able to use the last "sh" for the system call.
* The dlresolve payload must be crafted manually in the given structures. The addresses are aligned.
* Use magicMove to call the dlresolve function.

### Unintended by Robbert1978 (Discord tag)

One of the unintended solutions caught my interest, which is this one. The unintended solution consists of creating a 1 argument function call primitive. That's one creative way to do it.

Link for writeup/solver & blog: [Link](https://robbert1978.github.io/posts/SecurinetsQuals-2023/)
