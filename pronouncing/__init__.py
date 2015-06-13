from __future__ import print_function
import re
from pkg_resources import resource_stream

__author__ = 'Allison Parrish'
__email__ = 'allison@decontextualize.com'
__version__ = '0.1.1'

pronunciations = None


def parse_cmu(cmufh):
    """Parses an incoming file handle as a CMU pronouncing dictionary file.

    (Most end-users of this module won't need to call this function explicitly,
    as it's called internally by the :func:`init_cmu` function.)

    :param cmufh: a filehandle with CMUdict-formatted data
    :returns: a list of 2-tuples pairing a word with its phones (as a string)
    """
    pronunciations = list()
    for line in cmufh:
        line = line.strip().decode('latin1')
        if line.startswith(';'):
            continue
        word, phones = line.split("  ")
        word = re.sub(r'\(\d\)$', '', word.lower())
        pronunciations.append((word.lower(), phones))
    return pronunciations


def init_cmu(filehandle=None):
    """Initialize the module's pronunciation data.

    This function is called automatically the first time you attempt to use
    another function in the library that requires loading the pronunciation
    data from disk. You can call this function manually to control when and
    how the pronunciation data is loaded (e.g., you're using this module in
    a web application and want to load the data asynchronously).

    :param filehandle: a filehandle with CMUdict-formatted data
    :returns: None
    """
    global pronunciations
    if pronunciations is None:
        if filehandle is None:
            filehandle = resource_stream(__name__, 'cmudict-0.7b')
        pronunciations = parse_cmu(filehandle)
        filehandle.close()


def syllable_count(phones):
    """Count the number of syllables in a string of phones.

    To find the number of syllables in a word, call :func:`phones_for_word`
    first to get the CMUdict phones for that word.

    .. doctest::

        >>> import pronouncing
        >>> phones = pronouncing.phones_for_word("literally")
        >>> pronouncing.syllable_count(phones)
        4

    :param phones: a string containing space-separated CMUdict phones
    :returns: integer count of syllables in list of phones
    """
    return sum([phones.count(i) for i in '012'])


def phones_for_word(find):
    """Get the CMUdict phones for a given word.

    Because a given word might have more than one pronunciation in the
    dictionary, this function returns a list of all possible pronunciations.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.phones_for_word("permit")
        [u'P ER0 M IH1 T', u'P ER1 M IH2 T']

    :param find: a word to find in CMUdict.
    :returns: a list of phone strings that correspond to that word.
    """
    init_cmu()
    matches = list()
    for word, phones in pronunciations:
        if word == find:
            matches.append(phones)
    return matches


def stresses(s):
    """Get the vowel stresses for a given string of CMUdict phones.

    Returns only the vowel stresses (i.e., digits) for a given phone string.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.stresses(pronouncing.phones_for_word('obsequious')[0])
        u'0100'

    :param s: a string of CMUdict phones
    :returns: string of just the stresses
    """
    return re.sub(r"[^012]", "", s)


def stresses_for_word(find):
    """Get a list of possible stress patterns for a given word.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.stresses_for_word('permit')
        [u'01', u'12']

    :param find: a word to find
    :returns: a list of possible stress patterns for the given word.
    """
    phone_lists = phones_for_word(find)
    return list(map(stresses, phone_lists))


def rhyming_part(phones):
    """Get the "rhyming part" of a string with CMUdict phones.

    "Rhyming part" here means everything from the vowel in the stressed
    syllable nearest the end of the word up to the end of the word.

    .. doctest::

        >>> import pronouncing
        >>> phones = pronouncing.phones_for_word("purple")
        >>> pronouncing.rhyming_part(phones)
        u'ER1 P AH0 L'

    :param phones: a string containing space-separated CMUdict phones
    :returns: a string with just the "rhyming part" of those phones
    """
    idx = 0
    phones_list = phones.split()
    for i in reversed(range(0, len(phones_list))):
        if phones_list[i][-1] in ('1', '2'):
            idx = i
            break
    return ' '.join(phones_list[idx:])


def search(pattern):
    """Get words whose pronunciation matches a regular expression.

    This function Searches the CMU dictionary for pronunciations matching a
    given regular expression. (Word boundary anchors are automatically added
    before and after the pattern.)

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.search('ER1 P AH0')
        [u'interpolate', u'interpolated', u'purple', u'purples']

    :param pattern: a string containing a regular expression
    :returns: a list of matching words
    """
    init_cmu()
    matches = list()
    for word, phones in pronunciations:
        if re.search(r"\b" + pattern + r"\b", phones):
            matches.append(word)
    return matches


def search_stresses(pattern):
    """Get words whose stress pattern matches a regular expression.

    This function is a special case of :func:`search` that searches only the
    stress patterns of each pronunciation in the dictionary. You can get
    stress patterns for a word using the :func:`stresses_for_word` function.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.search_stresses('020120')
        [u'gubernatorial']

    :param pattern: a string containing a regular expression
    :returns: a list of matching words
    """
    init_cmu()
    matches = list()
    for word, phones in pronunciations:
        if re.search(pattern, stresses(phones)):
            matches.append(word)
    return matches


def rhymes(word):
    """Get words rhyming with a given word.

    This function may return an empty list if no rhyming words are found in
    the dictionary, or if the word you pass to the function is itself not
    found in the dictionary.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.rhymes("conditioner")
        [u'commissioner', u'parishioner', u'petitioner', u'practitioner']

    :param word: a word
    :returns: a list of rhyming words
    """
    all_rhymes = list()
    all_phones = phones_for_word(word)
    for phones_str in all_phones:
        part = rhyming_part(phones_str)
        rhymes = search(part + "$")
        all_rhymes.extend(rhymes)
    return [r for r in all_rhymes if r != word]
