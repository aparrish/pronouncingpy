Tutorial and Cookbook
=====================

This tutorial will demonstrate how to perform several common tasks with the
Pronouncing library and provide a few examples of how the library can be used
creatively.

Word pronunciations
-------------------

Let's start by using Pronouncing to get the pronunciation for a given word.
Here's the code::

    >>> import pronouncing
    >>> pronouncing.phones_for_word("permit")
    [u'P ER0 M IH1 T', u'P ER1 M IH2 T']

The :func:`pronouncing.phones_for_word` function returns a list of all
pronunciations for the given word found in the CMU pronouncing dictionary.
Pronunciations are given using a special phonetic alphabet known as ARPAbet.
`Here's a list of ARPAbet symbols and what English sounds they stand for
<http://www.speech.cs.cmu.edu/cgi-bin/cmudict#phones>`_. Each token in a
pronunciation string is called a "phone." The numbers after the vowels indicate
the vowel's stress. The number ``1`` indicates primary stress; ``2`` indicates
secondary stress; and ``0`` indicates unstressed. (`Wikipedia has a good
overview of how stress works in English
<https://en.wikipedia.org/wiki/Stress_and_vowel_reduction_in_English>`_, if
you're interested.)

Sometimes, the pronouncing dictionary has more than one pronunciation for the
same word. "Permit" is a good example: it can be pronounced either with the
stress on the first syllable ("do you have a permit to program here?") or
on the second syllable ("will you permit me to program here?"). For this
reason, the :func:`pronouncing.phones_for_word` function returns a list of
possible pronunciations. (You'll need to come up with your own criteria for
deciding which pronunciation is best for your purposes.)

Here's how to calculate the most common sounds in a given text::

    >>> import pronouncing                                            
    >>> from collections import Counter                               
    >>> text = "april is the cruelest month breeding lilacs out of the dead"
    >>> count = Counter()                                             
    >>> words = text.split()
    >>> for word in words:
    ...   pronunciation_list = pronouncing.phones_for_word(word)
    ...   if len(pronunciation_list) > 0:
    ...     count.update(pronunciation_list[0].split(" "))
    ... 
    >>> count.most_common(5)
    [(u'AH0', 4), (u'L', 4), (u'D', 3), (u'R', 3), (u'DH', 2)]

Pronunciation search
--------------------

Pronouncing has a helpful function :func:`pronouncing.search` which allows you
to search the pronouncing dictionary for words whose pronunciation matches a
particular regular expression. For example, to find words that have within them
the same sounds as the word "sighs"::

    >>> import pronouncing
    >>> phones = pronouncing.phones_for_word("sighs")[0]
    >>> pronouncing.search(phones)[:5]
    [u'incise', u'incised', u'incisor', u'incisors', u'malloseismic']

For convenience, word-boundary anchors (``\b``) are added automatically to the
beginning and end of the pattern you pass to :func:`pronouncing.search`. You're
free to include any other regular expression syntax in the pattern. Here's
another example, which finds all of the words that end in "-iddle"::

    >>> pronouncing.search("IH1 D AH0 L$")[:5]
    [u'biddle', u'criddle', u'fiddle', u'friddle', u'kiddle']

Another example, which re-writes a text by taking each word and replacing it
with a random word that begins with the same first two phones::

    >>> import pronouncing
    >>> import random
    >>> text = 'april is the cruelest month breeding lilacs out of the dead'
    >>> out = list()
    >>> for word in text.split():
    ...   phones = pronouncing.phones_for_word(word)[0]
    ...   first2 = phones.split()[:2]
    ...   out.append(random.choice(pronouncing.search("^" + " ".join(first2))))
    ... 
    >>> print ' '.join(out)
    apec's isn't them kraatz muffy bronte leichliter outpacing of than delfs

Counting syllables
------------------

To get the number of syllables in a word, first get one of its pronunciations
with :func:`pronouncing.phones_for_word` and pass the resulting string of
phones to the :func:`pronouncing.syllable_count` function, like so::

    >>> import pronouncing
    >>> pronunciation_list = pronouncing.phones_for_word("programming")
    >>> pronouncing.syllable_count(pronunciation_list[0])
    3

The following example calculates the total number of syllables in a text
(assuming that all of the words are found in the pronouncing dictionary)::

    >>> import pronouncing
    >>> text = "april is the cruelest month breeding lilacs out of the dead"
    >>> phones = [pronouncing.phones_for_word(p)[0] for p in text.split()]
    >>> sum([pronouncing.syllable_count(p) for p in phones])
    15

Meter
-----

Pronouncing includes a number of functions to help you isolate metrical
characteristics of a text. You can use the :func:`pronouncing.stresses`
function to get a string that represents the "stress pattern" of a string of
phones::

    >>> import pronouncing
    >>> phones_list = pronouncing.phones_for_word("snappiest")
    >>> pronouncing.stresses(phones_list[0])
    u'102'

A "stress pattern" is a string that contains only the stress values from a
sequence of phones. (The numbers indicate the level of stress: ``1`` for
primary stress, ``2`` for secondary stress, and ``0`` for unstressed.)

You can use the :func:`pronouncing.search_stresses` function to find words based on their
stress patterns. For example, to find words that have two dactyls in them
("dactyl" is a metrical foot consisting of one stressed syllable followed by
two unstressed syllables)::

    >>> import pronouncing
    >>> pronouncing.search_stresses("100100")
    [u'afroamerican', u'afroamericans', u'interrelationship', u'overcapacity']

You can use regular expression syntax inside of the patterns you give to
:func:`pronouncing.search_stresses`. For example, to find all words wholly
consisting of two anapests (unstressed, unstressed, stressed), with "stressed"
meaning either primary stress or secondary stress::

    >>> import pronouncing
    >>> pronouncing.search_stresses("^00[12]00[12]$")
    [u'neopositivist', u'undercapitalize', u'undercapitalized']

The following example rewrites a text, replacing each word with a random word
that has the same stress pattern::

    >>> import pronouncing
    >>> import random
    >>> text = 'april is the cruelest month breeding lilacs out of the dead'
    >>> for word in text.split():
    ...   pronunciations = pronouncing.phones_for_word(word)
    ...   pat = pronouncing.stresses(pronunciations[0])
    ...   replacement = random.choice(pronouncing.search_stresses("^"+pat+"$"))
    ...   out.append(replacement)
    ... 
    >>> ' '.join(out)
    u"joneses kopf whats rathbun p's gavan midpoint nill goh the pont's"

Rhyme
-----

Pronouncing includes a simple function, :func:`pronouncing.rhymes`, which
returns a list of words that (potentially) rhyme with a given word. You can use
it like so::

    >>> import pronouncing
    >>> pronouncing.rhymes("failings")
    [u'mailings', u'railings', u'tailings']

The :func:`pronouncing.rhymes` function returns a list of all possible rhymes
for the given word---i.e., words that rhyme with any of the given word's
pronunciations. If you only want rhymes for one particular pronunciation, the
the :func:`pronouncing.rhyming_part` function gives a smaller part of a string
of phones that can be used with :func:`pronouncing.search` to find rhyming
words. The following code demonstrates how to find rhyming words for two
different pronunciations of "uses"::

    >>> import pronouncing
    >>> pronunciations = pronouncing.phones_for_word("uses")
    >>> sss = pronouncing.rhyming_part(pronunciations[0])
    >>> zzz = pronouncing.rhyming_part(pronunciations[1])
    >>> pronouncing.search(sss + "$")[:5]
    [u"bruce's", u'juices', u'medusas', u'produces', u"tuscaloosa's"]
    >>> pronouncing.search(zzz + "$")[:5]
    [u'abuses', u'cabooses', u'disabuses', u'excuses', u'induces']

Use the ``in`` operator to check to see if one word rhymes with another::

    >>> import pronouncing
    >>> "wheeze" in pronouncing.rhymes("cheese")
    True
    >>> "geese" in pronouncing.rhymes("cheese")
    False

The following example rewrites a text, replacing each word with a rhyming
word (when a rhyming word is available)::

    >>> import pronouncing                                                  
    >>> import random                                                       
    >>> text = 'april is the cruelest month breeding lilacs out of the dead'
    >>> out = list()
    >>> for word in text.split():
    ...   rhymes = pronouncing.rhymes(word)
    ...   if len(rhymes) > 0:
    ...     out.append(random.choice(rhymes))
    ...   else:
    ...     out.append(word)
    ... 
    >>> print ' '.join(out)
    april wiles's duh coolest month ceding pontiac's krout what've worthey wehde

Next steps
----------

Hopefully this is just the beginning of your rhyme- and meter-filled journey.
Consult :doc:`pronouncing` for more information about individual functions in the
library.

Pronouncing is just one possible interface for the CMU pronouncing dictionary,
and you may find that for your particular purposes, a more specialized
approach is necessary. In that case, feel free to `peruse Pronouncing's source
code <http://github.com/aparrish/pronouncingpy>`_ for helpful hints and
tidbits.

