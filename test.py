import unittest
import metrics


class TestHammingDistance(unittest.TestCase):

    def check_hamming_distance(self, a, b, expected):
        self.assertEqual(metrics.hamming_distance(a, b), expected)

    def test_hamming_distance(self):
        self.check_hamming_distance("karolin", "kathrin", 3)
        self.check_hamming_distance("karolin", "kerstin", 3)
        self.check_hamming_distance("1011101", "1001001", 2)
        self.check_hamming_distance("2173896", "2233796", 3)

    def test_empty(self):
        self.check_hamming_distance("", "", 0)
        self.check_hamming_distance("test", "", None)
        self.check_hamming_distance("", "test", None)


class TestLevenshteinDistance(unittest.TestCase):

    def check_levenshtein_distance(self, a, b, expected):
        self.assertEqual(metrics.levenshtein_distance(a, b), expected)

    def test_empty(self):
        self.check_levenshtein_distance("", "", 0)
        self.check_levenshtein_distance("a", "", 1)
        self.check_levenshtein_distance("", "a", 1)

    def test_equal(self):
        self.check_levenshtein_distance("a", "a", 0)
        self.check_levenshtein_distance("abcde", "abcde", 0)

    def test_levenshtein_distance(self):
        self.check_levenshtein_distance("kitten", "sitting", 3)
        self.check_levenshtein_distance("saturday", "sunday", 3)
        self.check_levenshtein_distance("casa", "cala", 1)
        self.check_levenshtein_distance("cala", "calla", 1)
        self.check_levenshtein_distance("rosettacode", "raisethysword", 8)


class TestDamearauLevenshteinDistance(unittest.TestCase):

    def check_damearau_levenshtein_distance(self, a, b, expected):
        self.assertEqual(metrics.damearau_levenshtein_distance(a, b), expected)

    def test_empty(self):
        self.check_damearau_levenshtein_distance("", "", 0)
        self.check_damearau_levenshtein_distance("", "a", 1)
        self.check_damearau_levenshtein_distance("a", "", 1)

    def test_equal(self):
        self.check_damearau_levenshtein_distance("a", "a", 0)
        self.check_damearau_levenshtein_distance("abcde", "abcde", 0)

    def test_damearau_levenshtein_distance(self):
        self.check_damearau_levenshtein_distance("ba", "abc", 2)
        self.check_damearau_levenshtein_distance("fee", "deed", 2)
        self.check_damearau_levenshtein_distance("abcd", "bacde", 3)


class TestLongestCommonSubsequence(unittest.TestCase):

    def check_lcs(self, a, b, expected):
        self.assertEqual(metrics.longest_common_subsequence(a, b), expected)

    def test_empty(self):
        self.check_lcs("", "", ("",))
        self.check_lcs("lol", "", ("",))
        self.check_lcs("", "lol", ("",))

    def test_longest_common_subsequence(self):
        self.check_lcs("1234", "1224533324", ("1234",))
        self.check_lcs("1224533324", "1234", ("1234",))
        self.check_lcs("thisisatest", "testing123testing", ("tsitest",))
        self.check_lcs("testing123testing", "thisisatest", ("tsitest",))

    # TODO: test multiple output


class TestJaroWinklerDistance(unittest.TestCase):

    def check_jkd(self, a, b, expected):
        self.assertEqual(metrics.jaro_winkler_distance(a, b), expected)

    def test_jaro_winkler_distance_edges(self):
        self.check_jkd("abc", "abc", 1)
        self.check_jkd("12345", "12345", 1)

        self.check_jkd("abc", "def", 0)
        self.check_jkd("lolol", "hueue", 0)

    def test_jaro_winkler_distance_decimal(self):
        self.check_jkd("abczhy", "abcdef", 0.5)
        self.check_jkd("123456", "456456", 0.5)


class TestKendellTauDistance(unittest.TestCase):

    def check_kendell_tau_distance(self, a, b, expected):
        self.assertEqual(metrics.kendall_tau_distance(a, b), expected)

    def test_kendell_tau_distance(self):
        self.check_kendell_tau_distance("ABCDE", "ABCDE", 0)
        self.check_kendell_tau_distance("ABLDE", "ABCDE", 2)
        self.check_kendell_tau_distance("FBCDE", "ABCDE", 4)
        self.check_kendell_tau_distance((1, 2, 3, 4, 5), (3, 4, 1, 2, 5), 4)


class TestDiceCoefficient(unittest.TestCase):

    # TODO
    def test_it(self):
        self.assertEqual(metrics.dice_coefficient("night", "nacht"), 0.25)

unittest.main()
