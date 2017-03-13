from __future__ import print_function
import re
from pkg_resources import resource_stream
import collections

__author__ = 'Allison Parrish'
__email__ = 'allison@decontextualize.com'
__version__ = '0.1.3'

pronunciations = None
lookup = None
rhymeDict = None


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
        pronunciations.append((word.rstrip('(0123456789)').lower(), phones))
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
    global pronunciations, lookup, rhymeDict
    if pronunciations is None:
        if filehandle is None:
            filehandle = resource_stream(__name__, 'cmudict-0.7b')
        pronunciations = parse_cmu(filehandle)
        filehandle.close()
        lookup = collections.defaultdict(list)
        for word, phones in pronunciations:
            lookup[word].append(phones)

        rhymeDict = collections.defaultdict(list)
        for word, phones in pronunciations:
            rp = rhyming_part(phones)
            if rp is not None:
                rhymeDict[rhyming_part(phones)].append(word)

def rhymesFast(word):
    """Get words rhyming with a given word.

    This function may return an empty list if no rhyming words are found in
    the dictionary, or if the word you pass to the function is itself not
    found in the dictionary.

    .. doctest::

        >>> import pronouncing
        >>> pronouncing.rhymesFast("conditioner")
        [u'commissioner', u'parishioner', u'petitioner', u'practitioner']

    :param word: a word
    :returns: a list of rhyming words
    """
    phones = phones_for_word(word)
    if not phones == []:
        rd = rhymeDict[rhyming_part(phones[0])]
        if word in rd:
            rd.pop(rd.index(word))
        return rd
    else:
        return []



def syllable_count(phones):
    """Count the number of syllables in a string of phones.

    To find the number of syllables in a word, call :func:`phones_for_word`
    first to get the CMUdict phones for that word.

    .. doctest::

        >>> import pronouncing
        >>> phones = pronouncing.phones_for_word("literally")
        >>> pronouncing.syllable_count(phones[0])
        4

    :param phones: a string containing space-separated CMUdict phones
    :returns: integer count of syllables in list of phones
    """
    return len(stresses(phones))


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
    return lookup.get(find, [])


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
        >>> pronouncing.rhyming_part(phones[0])
        u'ER1 P AH0 L'

    :param phones: a string containing space-separated CMUdict phones
    :returns: a string with just the "rhyming part" of those phones
    """
    phones_list = phones.split()
    for i in range(len(phones_list) - 1, 0, -1):
        if phones_list[i][-1] in '12':
            return ' '.join(phones_list[i:])
    return phones


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
    regexp = re.compile(r"\b" + pattern + r"\b")
    return [word
            for word, phones in pronunciations
            if regexp.search(phones)]


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
    regexp = re.compile(pattern)
    return [word
            for word, phones in pronunciations
            if regexp.search(stresses(phones))]


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
    for phones_str in phones_for_word(word):
        part = rhyming_part(phones_str)
        rhymes = search(part + "$")
        all_rhymes.extend(rhymes)
    return [r for r in all_rhymes if r != word]
