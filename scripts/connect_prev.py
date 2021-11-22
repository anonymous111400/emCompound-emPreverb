"""
Less primitive way to connect preverbs to verbs.
Using advanced itertools techniques. :)
"""

import sys
import argparse
import json

from itertools import chain
from more_itertools import split_at, windowed

from word import stream_to_word_objects, Word, WORD_SEPARATOR

ENV = 2 # search for [/Prev] in a -env..env environment of the [/V]

VERB_POSTAG = '[/V]'
PREVERB_POSTAG = '[/Prev]'
ADVERB_POSTAG = '[/Adv]'


def add_preverb(verb, args, preverb=None):
    """Update *verb* with info from *preverb*."""
    verb.xpostag = PREVERB_POSTAG + verb.xpostag
    if preverb is not None:
        vlemma = verb.lemma.lower()

        args.prev_id += 1
        previd = str(args.prev_id)

        # handle verb
        verb.lemma = preverb.lemma + vlemma
        if 'compound' in Word.features:
            verb.compound = preverb.lemma + '#' + vlemma
        verb.separated = 'sep'
        verb.previd = previd

        # handle preverb
        if args.add_verb_lemma:
            preverb.lemma += '[' + vlemma + ']'
        else:
            # empty lemma for connected preverb
            preverb.lemma = ''
        if 'compound' in Word.features:
            preverb.compound = preverb.lemma
        preverb.separated = 'conn'
        preverb.previd = previd
    else:
        verb.separated = 'pfx'


def contains_preverb(verb):
    """
    Check whether the verb form contains a preverb according to
    the analysis selected by the pos tagger.
    """
    anas_list = json.loads(verb.anas)
    for ana in anas_list:
        if ana["lemma"] == verb.lemma and ana["tag"] == verb.xpostag:
            last_good_ana = ana
    return PREVERB_POSTAG in last_good_ana['readable']


def main():
    """Main."""

    args = get_args()
    args.prev_id = 0

    header = next(sys.stdin)
    Word.features = header.strip().split('\t')

    INPUT_FIELDS = {'form', 'lemma', 'xpostag'}
    if not INPUT_FIELDS <= set(Word.features):
        raise ValueError('Required column(s) ' +
                         str(INPUT_FIELDS - set(Word.features)) +
                         ' missing from input')

    # add 'separated' and 'previd' fields
    Word.features.append('separated')
    Word.features.append('previd')
    print(Word(Word.features)) # print header

    lines = (x.rstrip('\n') for x in sys.stdin)
    sentences = split_at(lines, lambda x: x == WORD_SEPARATOR)

    window_size = 2 * ENV + 1
    center = ENV # index of central element in window

    fakeword = Word([''] * len(Word.features))
    padding = [fakeword] * ENV

    for sentence in sentences:

        # add empty 'separated' and 'previd' values
        sentence = [line + '\t\t' for line in sentence]

        word_objects = stream_to_word_objects(sentence)
        padded_sentence = chain(padding, word_objects, padding) # !

        processed = []

        for window in windowed(padded_sentence, window_size): # !

            left = list(reversed(window[:center+1])) # abc..
            central = window[center]                 # ..c..
            right = window[center:]                  # ..cde

            if (central.xpostag.startswith(VERB_POSTAG)
                    and VERB_POSTAG in central.anas  # az anas szerint is ige?
                    and central.form != "volna"):

                # 1. eset: eleve igekötős -- egyszerűen van-e [/Prev] az ANAS-ban
                if (PREVERB_POSTAG in central.anas and contains_preverb(central)):
                    add_preverb(central, args)

                # 2. eset: "szét" [msd="IGE.*|HA.*"] [msd="IGE.*" & word != "volna"]
                # szét kell szerelni, szét se szereli
                elif (left[2].xpostag == PREVERB_POSTAG and
                      left[1].xpostag.startswith((ADVERB_POSTAG, VERB_POSTAG))):
                    add_preverb(central, args, left[2])

                # 3. eset: [msd="IGE.*" & word != "volna] "szét"
                elif right[1].xpostag == PREVERB_POSTAG:
                    add_preverb(central, args, right[1])

                # 4. eset: [msd="IGE.*" & word != "volna] [msd="HA.*" | word="volna"] "szét"
                # rágja is szét, rágta volna szét, tépi hirtelen szét
                elif (right[2].xpostag == PREVERB_POSTAG and
                        (right[1].xpostag.startswith(ADVERB_POSTAG)
                         or right[1].form == 'volna')
                      ):
                    add_preverb(central, args, right[2])

                # nem igekötős
                else:
                    pass

            # should be collected before printing
            # because left[2] can change if it is a preverb!
            processed.append(central)

        for word in processed:
            print(word)

        print(WORD_SEPARATOR)


def get_args():
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--add-verb-lemma', '-v',
        help=('append the verb\'s lemma in brackets to ' +
              'the connected preverb\'s lemma'),
        action='store_true'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
