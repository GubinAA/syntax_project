

from natasha import (
    Segmenter,
    NewsSyntaxParser,
    NewsEmbedding,
    Doc
)



word_dict = {
    'root': 'сказуемое',
    'amod': 'определение',
    'punct': 'знак препинания',
    'conj': 'союз',
    'nsubj': 'подлежащее',
    'obj': 'дополнение',
    'advmod': 'обстоятельство',
    'xcomp': 'сказуемое',
    'iobj': 'определение',
    'case': 'предлог',
    'obl': 'обстоятельство',
    'cc' : 'союз',
    'nmod': 'дополнение',
    'appos': 'дополнение',
    'det': 'определение',
    'cop': 'сказуемое',
    'csubj': 'сказуемое'
            }


def syntax_func(text:str):
    #Обработка языка
    emb = NewsEmbedding()
    segmenter = Segmenter()
    syntax_parser = NewsSyntaxParser(emb)
    doc = Doc(text)
    doc.segment(segmenter)
    doc.parse_syntax(syntax_parser)
    word_list = [list(i) for i in doc.tokens]
    word_output = []
    for i in word_list:
        try:
            word_output += [str(i[2]) + '-' + str(word_dict[i[5]])]
        except:
            word_output += [str(i[2]) + '-' + str(i[5])]

    return word_output
