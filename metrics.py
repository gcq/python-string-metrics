import itertools


def hamming_distance_positions(a, b):
    """Return the positions at which two strings differ using the Hamming method

    In information theory, the Hamming distance between two strings
    of equal length is the number of positions at which
    the corresponding symbols are different.
    In another way, it measures the minimum number of substitutions required
    to change one string into the other, or the minimum number of errors
    that could have transformed one string into the other.

    Notes: Inputs must be same length or None will be returned
    """

    # Output for inputs of different length is undefined
    if len(a) != len(b):
        return None

    # This will hold the indexes at which the inputs differ
    positions = []
    for pos, pair in enumerate(zip(a, b)):
        if pair[0] != pair[1]:
            positions.append(pos)

    return positions


def hamming_distance(a, b):
    """Return the Hamming distance for two strings

    See: hamming_distance_positions
    """

    hamming = hamming_distance_positions(a, b)

    try:
        return len(hamming)
    except TypeError:
        return None


def levenshtein_distance(a, b):
    """Returns the Levenshtein distance between the two input strings.

    In information theory and computer science, the Levenshtein distance is
    a string metric for measuring the difference between two sequences.
    Informally, the Levenshtein distance between two words is the minimum
    number of single-character edits (insertions, deletions or substitutions)
    required to change one word into the other.
    """

    if len(a) == 0:
        return len(b)

    if len(b) == 0:
        return len(a)

    # Bi-dimensional array initialized to zeroes
    table = [[0 for o in range(len(b) + 1)] for i in range(len(a) + 1)]

    # Headers of columns
    for i in range(len(a)):
        table[i][0] = i

    # and rows
    for i in range(len(b)):
        table[0][i] = i
    # for the starting comparisons

    # Iterate over rows
    for a_index, a_item in enumerate(a):
        # Don't touch headers
        a_index += 1

        # Iterate over columns
        for b_index, b_item in enumerate(b):
            # headers again
            b_index += 1

            # cost is 1 if different value else 0
            cost = not a_item == b_item

            d = table[a_index - 1][b_index] + 1         # deletion
            i = table[a_index][b_index - 1] + 1         # inserion
            s = table[a_index - 1][b_index - 1] + cost  # substitution

            table[a_index][b_index] = min(d, i, s)

    # The last cell contains the distance
    return table[-1][-1]


def damearau_levenshtein_distance(a, b):
    """Returns the Damerau–Levenshtein distance between two strings

    The name Damerau–Levenshtein distance is used to refer to the
    edit distance that allows multiple edit operations including transpositions

    See: levenshtein_distance
    """

    if len(a) == 0:
        return len(b)

    if len(b) == 0:
        return len(a)

    # Bi-dimensional array initialized to zeroes
    table = [[0 for o in range(len(b) + 1)] for i in range(len(a) + 1)]

    # Headers of columns
    for i in range(len(a)):
        table[i][0] = i

    # and rows
    for i in range(len(b)):
        table[0][i] = i
    # for the starting comparisons

    # Iterate over rows
    for a_idx, a_item in enumerate(a):
        # Don't touch headers
        a_idx += 1

        # Iterate over columns
        for b_idx, b_item in enumerate(b):
            # headers again
            b_idx += 1

            # cost is 1 if different value else 0
            cost = not a_item == b_item

            d = table[a_idx - 1][b_idx] + 1         # deletion
            i = table[a_idx][b_idx - 1] + 1         # inserion
            s = table[a_idx - 1][b_idx - 1] + cost  # substitution
            t = table[a_idx - 2][b_idx - 2] + cost  # transposition

            # Only take care of transposition if we are advanced on the inputs
            # and the operation is possible with said characters.
            # We take 2 instead of one to get the previous char, because
            # the idx is 1-based, and strings are 0-idxed
            if a_idx and a_item == b[b_idx - 2] == a[a_idx - 2] == b_item:
                table[a_idx][b_idx] = min(d, i, s, t)
            else:
                table[a_idx][b_idx] = min(d, i, s)

    # The last cell contains the distance
    return table[-1][-1]

# Alias
optimal_string_alignment_distance = damearau_levenshtein_distance


def longest_common_subsequence(c, r):
    """Returns a tuple with the Longest common sequences

    The longest common subsequence (or LCS) of groups A and B
    is the longest group of elements from A and B that are common
    between the two groups and in the same order in each group.

    Note: Both inputs must be length >= 1 if not a sequence containing
          an empty string wil be returned
    """

    # Empty strings symbolize None

    # If either one of the inputs is empty, return an empty string
    if not c or not r:
        return ("",)

    # Initialize the bi-dimensional array with lists containing empty strings
    # Has to be one unit bigger for both sides because:
    table = [[[""] for o in range(len(c) + 1)] for i in range(len(r) + 1)]

    for r_index, r_item in enumerate(r):
        # we never want to use row 0, as it is used for the first check
        r_index += 1

        for c_index, c_item in enumerate(c):
            # Same here
            c_index += 1

            if c_item == r_item:
                # If both collections are the same, prepend the top-left cell
                # to each item in the collection
                topleft = table[r_index - 1][c_index - 1]
                this = [i + c_item for i in topleft]
                table[r_index][c_index] = this

            else:
                # Else get the directly top and left cells to check against
                above = table[r_index - 1][c_index]
                left = table[r_index][c_index - 1]

                if len(above) == 1 and len(left) == 1:
                    # If both collections have only one item
                    above = above[0]
                    left = left[0]

                    # Get the maximum length
                    length = max((len(above), len(left)))

                    # And set the current cell to all the items that have
                    # that length
                    longest = [i for i in (above, left) if len(i) == length]

                else:
                    # If the collection has more than one item
                    # combine the two without adding duplicates
                    longest = above + [i for i in left if i not in above]

                table[r_index][c_index] = longest

    # The output f the function is the
    # longest item/items in the last cell's collection
    maxlen = max(map(len, table[-1][-1]))
    return tuple(set(i for i in table[-1][-1] if len(i) == maxlen))


# See http://stackoverflow.com/q/2631726/2065904
def longest_increasing_subsequence(a):
    """Returns a tuple with the Longest increasing subsequences

    In computer science, the longest increasing subsequence problem is to find
    a subsequence of a given sequence in which the subsequence's elements
    are in sorted order, lowest to highest, and in which the subsequence is
    as long as possible.
    This subsequence is not necessarily contiguous, or unique.
    """
    pass  # TODO


# Translated from http://stackoverflow.com/q/19123506/2065904
def jaro_winkler_distance(a, b):
    """Returns the Jaro–Winkler distance

    http://en.wikipedia.org/wiki/Jaro–Winkler_distance

    A type of string edit distance, mainly used in the area of
    duplicate detection. The higher the Jaro–Winkler distance
    for two strings is, the more similar the strings are.
    The Jaro–Winkler distance metric is designed and best suited for
    short strings such as person names.
    The score is normalized such that 0 equates to no similarity and
    1 is an exact match.
    """
    # TODO: Understand what this does and comment src
    # (not a lot of info online :/)

    weight_threshold = 0.7
    num_chars = 4

    if len(a) == 0:
        return 1.0 if len(b) == 0 else 0.0

    matched1 = [False for i in range(len(a))]
    matched2 = [False for i in range(len(b))]

    num_common = 0
    for a_index, a_item in enumerate(a):
        for b_index, b_item in enumerate(b):
            if a_item != b_item:
                continue

            matched1[a_index] = True
            matched2[b_index] = True

            num_common += 1

            break

    if num_common == 0:
        return 0.0

    transposed = 0
    k = 0
    for a_index, a_item in enumerate(a):
        if matched1[a_index]:
            continue

        while not matched2[k]:
            k += 1

        if a_item != b_item:
            transposed += 1

        k += 1

    transposed = transposed / 2

    weight = (
        (num_common / len(a)) +
        (num_common / len(b)) +
        ((num_common - transposed) / num_common)
    ) / 3.0

    if weight <= weight_threshold:
        return weight

    m = min((num_chars, len(a), len(b)))
    pos = 0
    while pos < m and a[pos] == b[pos]:
        pos += 1

    if pos == 0:
        return weight
    else:
        return weight + 0.1 * pos * (1 - weight)


def kendall_tau_distance(a, b):
    """Returns the Kendell tau distance between two strings

    The Kendall tau rank distance is a metric that counts the number of
    pairwise disagreements between two ranking lists.
    The larger the distance, the more dissimilar the two lists are.
    Also called bubble-sort distance since it is equivalent to the number of
    swaps that the bubble sort algorithm would make to place one list
    in the same order as the other list.

    Note: Inputs must be same length if not None will be returned
    """

    # If inputs differ in length, undefined
    if len(a) != len(b):
        return None

    l = len(a)

    distance = 0

    for m in range(l):
        # Start the range at m, so we don't recheck pairs
        for n in range(m, l):
            if (a[m] < a[n]) != (b[m] < b[n]):
                distance += 1

    return distance

# Alias
bubble_sort_distance = kendall_tau_distance


# TODO
def dice_coefficient(a, b):
    def makepairs(s):
        x, y = itertools.tee(s)
        next(y, None)
        return zip(x, y)

    a_pairs = tuple(makepairs(a))
    b_pairs = tuple(makepairs(b))

    intersection = 0
    union = len(a_pairs) + len(b_pairs)

    for a_pair in a_pairs:
        for b_pair in b_pairs:
            if a_pair == b_pair:
                intersection += 1

    return 2 * intersection / union
