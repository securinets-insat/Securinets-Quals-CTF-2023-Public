# 0-8-4

![Categorie](https://img.shields.io/badge/Category-Misc-red?style=for-the-badge) ![Level](https://img.shields.io/badge/Difficulty-Medium-yellow?style=for-the-badge)

![tags](https://img.shields.io/badge/Tag-Quantum%20computing-blue)

## Solution

* The given matrix corresponds to the Hamiltonian operator, you need to decompose it to its Pauli form first in order to work with it
* Second step is to do a Hamiltonian simulation to get the circuit corresponding to exp(-iHt), the solution for Shrodinger's equation with the trotter number equals 1 and t=1.
* Finally you get the circuit's unitary matrix and get the smallest eigenvalue for that matrix
* It can be done simpler by simulating the gates found from decomposing the Hamiltonian into its Pauli form and going from there but this code can help with almost any Hamiltonian, you can also find a lot of Hamiltonian simulation codes if you search.

## Description

>While on a mission, one of our teams discovered a weird suitecase locked with a 7-character password. The object had this matrix carved on its side, barely readable:
>
>            [ 0.7056    ,  0.         , 0.        ,  0.9        ]
>            [ 0.        ,  0.5318     , 0.168     ,  0.         ]
>            [ 0.        , 0.168       , -1.1246   ,  0.         ]
>            [ 0.9       ,  0.         , 0.        ,  0.7882     ]
>
>After analysis, we found out that the suitecase was emitting a transmission containing more informations, and we are convinced that the password is supposed to be the real part of the smallest eigenvalue, that needs to be calculated from the unitary matrix of the quantum circuit which corresponds to some simulation of suitcase matrix. The transmission also stated some weird conditions: the totter number is 1 and the simulation is done at t=1??? I don't know what that means exacly but I figured maybe you will?
>
>Flag format: Securinets{XXXXXXX}
>
>Author: mida0ui
