crypt_solver
=============
A simple Python script to help solve simple-substition ciphers.

Usage
-----
python3 crypt_solver.py <ciphertext> [--dictionary dictionary_file]

Details
-------
This simple Python script provides a tool for solving simple-substition ciphers
where each letter in the ciphertext represents one plaintext letter, and
each plaintext letter is represented by exactly one ciphertext letter.

It works by figuring out the possible matches for each of the ciphertext words,
given a dictionary lookup, and then finding scenarios where a potential
substitution key holds true for all the entries.

Notes
-----
This is largely an opportunity for me to dust off my Python skills while
also making something that may be of use in puzzle-solving.
