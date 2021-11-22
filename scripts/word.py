"""
Class representing words.
"""

from types import SimpleNamespace

WORD_SEPARATOR = ''

# legacy
_CNT_FIELDS = 5
FORM, WSAFTER, ANAS, _LEMMA, _XPOSTAG = list(range(_CNT_FIELDS))


class Word(SimpleNamespace):
    """Represent emtsv columns as object attributes"""

    features = ['form', 'wsafter', 'anas', 'lemma', 'xpostag']

    @classmethod
    def header(cls):
        """Return tsv format column headers"""
        return '\t'.join(cls.features)

    def __init__(self, args):
        """Construct word object from list of emtsv feature values"""
        if len(args) != len(self.features):
            raise RuntimeError(f"{len(self.features)} features expected, "
                               + f"{len(args)} provided")

        super().__init__(**dict(zip(self.features, args)))

    def __str__(self):
        """Return tsv format representation of word object."""
        return '\t'.join(self.__dict__.values())


class PseudoWord(Word):
    """Encode annotation as an emtsv token; ignore these when detokenizing!"""

    pass


def stream_to_word_objects(stream):
    """Process stream containing tsv format stripped lines."""
    for line in stream:
        yield Word(line.split('\t'))


# legacy
def stream_to_words(stream):
    """Process line: split by TAB + handle empty lines."""
    for line in stream:
        line = line.rstrip('\n')
        yield line.split('\t') if line != WORD_SEPARATOR else WORD_SEPARATOR


# legacy
def word_to_line(word):
    """Create a line from word."""
    return '\t'.join(word)
