from difflib import SequenceMatcher
from heapq import nlargest as _nlargest


def get_close_matches_indexes(word: str, possibilities: list, n=3, cutoff=0.6):
    """
    Позволяет найти индексы наилуших совпадений со словом в заданном списке.
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))

    elif not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))

    else:
        result = []
        s = SequenceMatcher()
        s.set_seq2(word)
        for idx, x in enumerate(possibilities):
            s.set_seq1(x)
            if s.real_quick_ratio() >= cutoff and \
                    s.quick_ratio() >= cutoff and \
                    s.ratio() >= cutoff:
                result.append((s.ratio(), idx))

        result = _nlargest(n, result)

        return [x for score, x in result]
