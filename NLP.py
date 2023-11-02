

from natasha import (
    Segmenter,
    NewsSyntaxParser,
    NewsMorphTagger,
    NewsEmbedding,
    Doc
)



word_dict = {
    'root': 'сказуемое',
    'amod': 'определение',
    'punct': 'знак препинания',
    'nsubj': 'подлежащее',
    'obj': 'дополнение',
    'advmod': 'обстоятельство',
    'xcomp': 'сказуемое',
    'iobj': 'определение',
    'case': 'предлог',
    'obl': 'дополнение',
    'cc' : 'союз',
    'appos': 'дополнение',
    'det': 'определение',
    'cop': 'сказуемое',
    'csubj': 'подлежащее',
    'discourse': 'вводное слово',
    'mark': 'предлог',
    'parataxis': 'сказуемое',
    'flat:name': 'Имя: дополнение или подлежащее',
    'acl': 'определение',
    'ccomp' : 'сказуемое',
    'advcl' : 'обстоятельство',
    'nummod:gov' : 'числительное',
    'fixed' : 'обстоятельство', #Я не уверен
    'nsubj:pass' : 'подлежащее', #Я не уверен
    'aux:pass' : 'определение', #Я не уверен
    'aux' : 'определение', #Я не уверен
    'obl:agent' : 'дополнение', #Я не уверен
    'expl' : 'дополнение', #Я не уверен
    'acl:relcl': 'сказуемое', #Я не уверен
    'nummod:entity' : 'числительное',
    'nummod' : 'числительное'
            }

nmod_dict = {
    'NOUN' : 'обстоятельство',
    'DET' : 'определение',
    'PRON' : 'определение',
    'ADP' : 'определение',
    'PROPN' : 'определение',
    'ADJ' : 'определение',
    'VERB' : 'сказуемое'
}

conj_dict = {
    'NOUN' : 'дополнение',
    'VERB' : 'сказуемое',
    'CCONJ' : 'союз',
    'ADJ' : 'определение',
    'NUM' : 'числительное',
    'PRON' : 'определение'
}

csubj_dict = {
    'NOUN' : 'подлежащее',
    'VERB' : 'сказуемое',
}

def syntax_func(text:str):
    #Обработка языка
    emb = NewsEmbedding()
    segmenter = Segmenter()
    syntax_parser = NewsSyntaxParser(emb)
    morph_tagger = NewsMorphTagger(emb)
    doc = Doc(text)
    doc_2 = Doc(text)
    doc_2.segment(segmenter)
    doc.segment(segmenter)
    doc.parse_syntax(syntax_parser)
    doc_2.tag_morph(morph_tagger)
    token_list = [list(i1) + list(i2) for i1, i2 in zip(doc.tokens, doc_2.tokens)]
    word_output = []
    for i in token_list:
        try:
            if i[5] == "nmod":
                word_output += [str(i[2]) + ' - ' + str(nmod_dict[i[15]])]
            elif i[5] == "conj":
                word_output += [str(i[2]) + ' - ' + str(conj_dict[i[15]])]
            elif i[5] == "csubj":
                word_output += [str(i[2]) + ' - ' + str(csubj_dict[i[15]])]
            else:
                word_output += [str(i[2]) + ' - ' + str(word_dict[i[5]])]
        except:
            word_output += [str(i[2]) + ' - ' + str(i[5]) + ' ' + str(i[15])]

    return word_output