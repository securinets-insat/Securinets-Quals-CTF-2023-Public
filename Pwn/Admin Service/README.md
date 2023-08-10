# Admin Service

## Solver

Ref: [Solver](./solver.py)

Notes:

* Leak everything using `/proc/self/maps`.
* Use `updateConfig` function to gain an arbitrary write. There is no upper bound check for the index.
* Write a shellcode/gadget in executeable area.
* Toggle the execution of the "backupCall" by writing "backup: 1" to the config.
* Execute backup.
