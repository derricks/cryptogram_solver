cryptogram_solver
=============
Various Python scripts for helping with cryptograms

  * crypt_solver.py: A simple Python script to help solve simple-substition ciphers.
  * vigenere.py: Encode or decode ciphers using a Vigenere cipher

Usage
-----
python3 crypt_solver.py <ciphertext> [--dictionary dictionary_file]
python3 vigenere.py -a encode|decode -k key-text ciphertext

Details
-------
crypt_solver.py

This simple Python script provides a tool for solving simple-substition ciphers
where each letter in the ciphertext represents one plaintext letter, and
each plaintext letter is represented by exactly one ciphertext letter.

It works by figuring out the possible matches for each of the ciphertext words,
given a dictionary lookup, and then finding scenarios where a potential
substitution key holds true for all the entries.

vigenere.py

This script takes a key and uses the Vigenere cipher to encode it

Notes
-----
This is largely an opportunity for me to dust off my Python skills while
also making something that may be of use in puzzle-solving.
