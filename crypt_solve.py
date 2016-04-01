import argparse
# Makes a best effort to solve a simple substitution cryptogram

def crypt(input_string):
    '''Convert a string to a cryptographic pattern. For instance, banana becomes 123232

   Args:
       input_string: the string to Convert

   Returns:
       the cryptographic pattern of the string
    '''
    max_mapping = 1
    mappings = dict()

    for current_character in input_string:
        if not current_character in mappings:
            mappings[current_character] = str(max_mapping)
            max_mapping = max_mapping + 1
    result = "".join([mappings[character] for character in input_string])
    return result

def find_crypt_matches(find_string, dictionary_file):
    '''Find all the words in a dictionary file that have the
    same cryptographic pattern as the search string.

    Args:
        find_string: the string to match against
        dictionary_file: the file to use for finding matches

    Returns:
        set of words in the dictionary file that have the same pattern as the search word
    '''

    crypt_to_match = crypt(find_string.lower())
    with open(dictionary_file) as file:
        return [match.strip().lower() for match in file if crypt(match.strip().lower()) == crypt_to_match]

def matches_per_word(phrase, dictionary_file):
    '''For each word in a phrase, find the matches.

    Args:
        phrase: a sequence of words on which to match
        dictionary_file: the file to use for finding matches for each word

    Returns:
        a dictionary of phrase word to cryptographic matches
    '''

    return {word.lower():find_crypt_matches(word, dictionary_file) for word in phrase.split(' ')}

def crypt_word_matches_plaintext_with_key(crypt_word, plain_word, key):
    '''Determines whether or not a cryptographic string
    maps to a plaintext word given a dictionary of cipher -> plain
    mappings.

    Args:
        crypt_word: the cryptogram text to check
        plain_word: the plaintext word to check against
        key: the current state of the cipher -> plain key to use for checking that the strings are plausible matches

    Returns:
        True if the plaintext word could be a match for the ciphertext word given the current key, False otherwise
    '''

    for crypt_index in range(0, len(crypt_word)):
        if crypt_word[crypt_index] in key and plain_word[crypt_index] != key[crypt_word[crypt_index]]:
            return False
    return True

def update_key_from_crypt_and_plain(crypt_word, plain_word, starting_key):
    '''
    Create a new cipher -> plain key that uses a ciphertext word, a plaintext equivalent
    and a starting_key. Any letters in the ciphertext that are not currently represented
    in the key will be added. Note that letters that are already mapped will be skipped.
    It us up to the caller to ensure the key is in the correct state
    (see  crypt_word_matches_plaintext_with_key)

    Args:
        crypt_word: the ciphertext word to us when building the key
        plain_word: the plaintext word that can be used to update the key
        starting_key: the current state of the cipher -> plain key

    Returns:
        a new key representing any cipher characters that can be mapped to plaintext
    '''

    # make a copy of the current key
    new_key = starting_key.copy()
    for crypt_index in range(0, len(crypt_word)):
        if not crypt_word[crypt_index] in new_key:
            new_key[crypt_word[crypt_index]] = plain_word[crypt_index]
    return new_key

def find_valid_keys(remaining_ciphers, current_solutions):
    '''Find any valid keys for the remaining ciphers.

    This function gets called recursively as it tries to
    find valid keys for the remaining set of ciphers. For
    each possible match, it checks against the existing keys
    to see if that combination would still be valid.
    If so, it updates the necessary arguments and
    calls this method again.

    Args:
        remaining_ciphers: the ciphers still to be checked
        current_solutions: a list of keys that are potentially valid

    Returns:
        the list of keys that are workable, or None
    '''

    # end-result case for recursion. If there are no more ciphers
    # then we've found valid solutions.
    if len(remaining_ciphers) == 0:
        return current_solutions

    return_solutions = []

    # doesn't matter what this word is; we just need to progress
    any_cipher = list(remaining_ciphers.keys())[0]
    possible_matches = remaining_ciphers[any_cipher]

    # create the reduced set of ciphers to search through
    reduced_ciphers = remaining_ciphers.copy()
    del reduced_ciphers[any_cipher]

    # for each current match and each key that could work
    # check to see if the match works. If it does
    # create a new candidate key and drill down
    for match in possible_matches:
        for key in current_solutions:
            if crypt_word_matches_plaintext_with_key(any_cipher, match, key):
                updated_key = update_key_from_crypt_and_plain(any_cipher, match, key)
                results = find_valid_keys(reduced_ciphers, [updated_key])
                if results != None:
                    # flatten returned array so that we don't have arrays of arrays
                    return_solutions = return_solutions + results

    return return_solutions if len(return_solutions) != 0 else None



def find_solution_keys(cipherphrase, dict_file):
    '''Find possible solution keys for the cipherphrase.

    The main entry point for doing the work. This does the
    setup and collects all the solution keys that might work

    Args:
        cipherphrase: the phrase to find solution keys for
        dict_file: the file to use as the dictionary

    Returns:
        a list of solution keys that are consistent with the ciphertext
    '''
    cipher_matches = matches_per_word(cipherphrase, dict_file)
    return find_valid_keys(cipher_matches, [{}])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Given a dictionary and a list of words, try and solve the cryptogram')
    argparser.add_argument('cipher_words', type=str, nargs='+',
        help='A list of ciphertext words to try and solve for')
    argparser.add_argument('--dictionary', type=str,
        help='The path to the dictionary file to use when solving. Defaults to /usr/shar/dict/words')

    parse_results = argparser.parse_args();
    ciphertext = ' '.join(parse_results.cipher_words).lower()
    dict_file = parse_results.dictionary if parse_results.dictionary else '/usr/share/dict/words'

    possible_keys = find_solution_keys(ciphertext, dict_file)
    if possible_keys == None:
        print('No solutions found')
    else:
        for key in possible_keys:
            print(''.join([key[cipher.lower()] if cipher in key else cipher for cipher in ciphertext]))
