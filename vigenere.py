import argparse

# constants

ASCII_MIN = 65

# create the vigenere grid
vigenere_dict_encode = dict()
vigenere_dict_decode = dict()
for character in range(26):
    mappings = { chr(key + ASCII_MIN):chr(((key + character) % 26) + ASCII_MIN) for key in range(26) }
    vigenere_dict_encode[chr(character + ASCII_MIN)] = mappings
    vigenere_dict_decode[chr(character + ASCII_MIN)] = { mappings[key]:key for key in mappings }

def repeating_key(key):
    '''Given a key string, generate the constituent letters in an infinite loop.

    For instance, LEMON will generate LEMONLEMONLEMO as needed.

    Args:
        key: string to cycle over

    Returns:
        generator that will return each letter in a loop
    '''
    current_character = 0
    while True:
        yield key[current_character]
        current_character = 0 if current_character == len(key) - 1 else current_character + 1

def encode(plaintext, key):
    '''For the given key, encode the passed-in string.

    Args:
        plaintext: the string to encode. any characters not in key will be left as-is
        key: the key to use for encoding

    Returns: the encoded string
    '''
    return _translate_with_key_and_dict_(plaintext, key, vigenere_dict_encode)

def decode(plaintext, key):
    '''For the given key, encode the passed-in string.

    Args:
        plaintext: the string to encode. any characters not in key will be left as-is
        key: the key to use for encoding

    Returns: the encoded string
    '''
    return _translate_with_key_and_dict_(plaintext, key, vigenere_dict_decode)

def _translate_with_key_and_dict_(plaintext, key, coding_dictionary):
    ''' Refactored code to handle translating plaintext with a given key based
    on a translation dictionary.

    Args:
        plaintext: a String of text to translate
        key: the key to use for lookups in the translation dictionary
        coding_dictionary: the translation mappings to use

    Returns: the translated string
    '''
    looping_key = repeating_key(key.upper())
    decoded_letters = [ (coding_dictionary[next(looping_key)][character] if character in coding_dictionary else character) for character in plaintext ]
    return ''.join(decoded_letters)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Encode or decode a string using the Vigenere cipher with the given key')
    argparser.add_argument('plaintext', type=str, nargs='+',
        help='A list of plaintext words to encode')
    argparser.add_argument('-k', type=str,
        help='The key to use for encoding the string')
    argparser.add_argument('-a', type=str, default='encode', choices=['encode','decode'],
        help='The action to take on the string. Must be eiher encode or decode.')

    args = argparser.parse_args();
    if (args.a == 'encode'):
        print(encode(' '.join(args.plaintext).upper(), args.k))
    else:
        print(decode(' '.join(args.plaintext).upper(), args.k))
