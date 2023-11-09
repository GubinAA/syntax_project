# NLP
# Имортируем библиотеку для обработки текста

from natasha import (
    Segmenter,
    NewsSyntaxParser,
    NewsMorphTagger,
    NewsEmbedding,
    Doc
)

#Словарь для перевода однозначных английских членов предложения в русские

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
    'fixed' : 'обстоятельство',
    'nsubj:pass' : 'подлежащее',
    'aux:pass' : 'определение',
    'aux' : 'определение',
    'obl:agent' : 'дополнение',
    'expl' : 'дополнение',
    'acl:relcl': 'сказуемое',
    'nummod:entity' : 'числительное',
    'nummod' : 'числительное'
            }

#Словарь для перевода nmod в русские члены предложения

nmod_dict = {
    'NOUN' : 'обстоятельство',
    'DET' : 'определение',
    'PRON' : 'определение',
    'ADP' : 'определение',
    'PROPN' : 'определение',
    'ADJ' : 'определение',
    'VERB' : 'сказуемое'
}

#Словарь для перевода conj в русские члены предложения

conj_dict = {
    'NOUN' : 'дополнение',
    'VERB' : 'сказуемое',
    'CCONJ' : 'союз',
    'ADJ' : 'определение',
    'NUM' : 'числительное',
    'PRON' : 'определение'
}

#Словарь для перевода csubj в русские члены предложения

csubj_dict = {
    'NOUN' : 'подлежащее',
    'VERB' : 'сказуемое',
}

def syntax_func(text:str):
    #Обработка языка
    emb = NewsEmbedding()
    #создаем сегментер
    segmenter = Segmenter()
    #создаем объект для обработки синтакситеческого состава
    syntax_parser = NewsSyntaxParser(emb)
    #создаем объект для обработки морфологического состава
    morph_tagger = NewsMorphTagger(emb)
    #переводим полученный текст в формат библиотеки
    doc = Doc(text)
    doc_2 = Doc(text)
    #cегментируем
    doc_2.segment(segmenter)
    doc.segment(segmenter)
    #получаем информацию о синтакситеческом составе предложения
    doc.parse_syntax(syntax_parser)
    #получаем информацию о морфологическом составе предложения
    doc_2.tag_morph(morph_tagger)
    #объединяем два списка
    token_list = [list(i1) + list(i2) for i1, i2 in zip(doc.tokens, doc_2.tokens)]
    #создаем выводной лист
    word_output = []
    #для каждого слова из полученного текста проверяем английский член предложения и при помощи словарей переводим в русские
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
    #возвращаем заполненный список
    return word_output