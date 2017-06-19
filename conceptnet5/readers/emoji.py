from conceptnet5.edges import make_edge
from conceptnet5.formats.msgpack_stream import MsgpackStreamWriter
from conceptnet5.uri import Licenses
from conceptnet5.nodes import standardized_concept_uri

import xml.etree.ElementTree as ET 


REL = '/r/SymbolOf'
DATASET = '/d/emoji'
LICENSE = Licenses.cc_attribution
SOURCE = [{'contributor': '/s/resource/unicode/cldr/31'}]


def is_sentence(text):
    """
    There are a few instances where a sentence of
    multiple words is used to describe an emoji
    (which is not very helpful in our case) AS WELL AS
    single words or phrases, which are separated by '|'.
    Using this function, we can ignore the sentences/phrases,
    and only look at single words, which is better for
    conceptnet to handle.
    """
    return (' ' in text and '|' not in text)


def strip_words(text):
    """
    When multiple words (not in a sentence, but
    separated by '|') are used to describe emojis,
    we need to remove the '|' in order to create
    edges for each word. This function takes out
    the '|' and puts all the words into a list.
    """
    return text.split(' | ')


def handle_file(input_file, output_file):
    tree = ET.parse(input_file)
    out = MsgpackStreamWriter(output_file)
    root = tree.getroot()
    lang = root[0][1].attrib['type']
    for annotation in root[1]:
    	if not is_sentence(annotation.text):
            start = standardized_concept_uri('mul', annotation.attrib['cp'])
            for word in strip_words(annotation.text):
                end = standardized_concept_uri(lang, word)
                edge = make_edge(REL, start, end, DATASET, LICENSE, SOURCE)
                out.write(edge)

