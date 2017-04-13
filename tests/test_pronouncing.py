import unittest
import pronouncing
import io


class TestPronouncing(unittest.TestCase):
    def test_parse_cmu(self):
        test_str = b"""\
;;; some test data to ensure that parsing CMU-formatted files works
ADOLESCENT  AE2 D AH0 L EH1 S AH0 N T
ADOLESCENT(1)  AE2 D OW0 L EH1 S AH0 N T
"""
        cmufh = io.BytesIO(test_str)
        pronunciations = pronouncing.parse_cmu(cmufh)
        self.assertTrue(len(pronunciations) > 0)
        matches = [x for x in pronunciations if x[0] == 'adolescent']
        self.assertEqual(len(matches), 2)

    def test_syllable_count(self):
        self.assertEqual(pronouncing.syllable_count("CH IY1 Z"), 1)
        self.assertEqual(pronouncing.syllable_count("CH EH1 D ER0"), 2)
        self.assertEqual(pronouncing.syllable_count("AE1 F T ER0 W ER0 D"), 3)
        self.assertEqual(
            pronouncing.syllable_count("IH2 N T ER0 M IH1 T AH0 N T"), 4)
        self.assertEqual(
            pronouncing.syllable_count("IH2 N T ER0 M IH1 T AH0 N T L IY0"),
            5)

    def test_phones_for_word(self):
        phones = pronouncing.phones_for_word("conflicts")
        self.assertEqual(len(phones), 4)
        self.assertEqual(phones[0], "K AH0 N F L IH1 K T S")
        # not in the dictionary (presumably)
        phones = pronouncing.phones_for_word("asdfasdfasdf")
        self.assertEqual(phones, [])

    def test_rhyming_part(self):
        part = pronouncing.rhyming_part("S L IY1 P ER0")
        self.assertEqual(part, "IY1 P ER0")
        part = pronouncing.rhyming_part("S L IY1 P AH0 L IY0")
        self.assertEqual(part, "IY1 P AH0 L IY0")
        part = pronouncing.rhyming_part("M ER0 M AE0 N S K")
        self.assertEqual(part, "M ER0 M AE0 N S K")

    def test_search(self):
        matches = pronouncing.search('^S K L')
        self.assertEqual(matches,
                         ['sclafani', 'scleroderma', 'sclerosis', 'sklar',
                             'sklenar'])
        matches = pronouncing.search('IH. \w* IH. \w* IH. \w* IH.')
        self.assertEqual(matches,
                         ['definitive', 'definitively', 'diminishes',
                             'diminishing', 'elicited', 'miscibility',
                             'primitivistic', 'privileges'])

    def test_rhymes(self):
        rhymes = pronouncing.rhymes("sleekly")
        expected = [
            'beakley', 'biweekly', 'bleakley', 'meekly', 'obliquely',
            'steakley', 'szekely', 'uniquely', 'weakley', 'weakly',
            'weekley', 'weekly', 'yeakley']
        self.assertEqual(expected, rhymes)
        # ensure correct behavior for words that don't rhyme
        rhymes = pronouncing.rhymes("orange")
        self.assertEqual([], rhymes)
        # ensure correct behavior for OOV words
        rhymes = pronouncing.rhymes("qwerasdfzxcv")
        self.assertEqual([], rhymes)

    def test_stresses(self):
        stresses = pronouncing.stresses('P ER0 M IH1 T')
        self.assertEqual('01', stresses)
        stresses = pronouncing.stresses('P ER1 M IH2 T')
        self.assertEqual('12', stresses)

    def test_stresses_for_word(self):
        stresses = pronouncing.stresses_for_word('permit')
        self.assertEqual(['01', '12'], stresses)

    def test_search_stresses(self):
        words = pronouncing.search_stresses('^000100$')
        self.assertEqual(
            words,
            ['phytogeography', 'uninterruptible', 'uninterruptible',
                'variability'])
        words = pronouncing.search_stresses('^[12]0[12]0[12]0[12]$')
        self.assertEqual(
            words,
            ['dideoxycytidine', 'homosexuality', 'hypersensitivity'])

if __name__ == '__main__':
    unittest.main()
