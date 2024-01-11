import pandas as pd
import spacy
from tqdm import tqdm
import json
from collections import OrderedDict
import ast

reram_data = pd.read_csv("ReRAM_DB_Final.csv")
print(len(reram_data))
nlp = spacy.load("en_core_web_trf")

Keyword_Json = OrderedDict()
'''1. 처음 ~ 끝 논문까지 for 문'''
clean_text = []
for index, row in tqdm(reram_data.iterrows()):
    title = row['title']
    if row['date'] == "[]":
        print(row['date'])

    '''2. 논문 정보를 Dictionary 형태로 저장'''
    Metadata = {
        # 'author':row['author'],
        # 'publisher':row['author'],
        'date': row['date'],
        # 'is-referenced-by-count':row['is-referenced-by-count'],
        # 'reference':row['reference'],
        # 'score':row['score'],
    }

    '''3. 동의어 처리한 Title 을 다시 Tokenize 하여 Keyword 로 저장'''
    clean_sentence = ""
    doc = nlp(title)
    for token in doc:

        '''3-1. 형용사 명사 고유명사 동사만을 Keyword 로 추출'''
        if token.pos_ in ["ADJ", "NOUN", "PROPN", "VERB"] and len(token.lemma_) > 1:
            keyword = token.lemma_
            clean_sentence += f" {keyword}"

            '''3-2. Keyword 에 Metadata 저장'''
            if not keyword in Keyword_Json:
                Keyword_Json[keyword] = []
            Keyword_Json[keyword].append(Metadata)


    '''4.논문의 Date 를 추가'''
    if not clean_sentence == "":
        clean_sentence += f"\t{ast.literal_eval(row['date'])[0]}"
        clean_text.append(clean_sentence)

'''5. JSON 데이터 저장'''
with open(f"ReRAM_Keywords_date.json", "w") as f:
    json.dump(Keyword_Json, f)

"""6. Title text 저장"""
with open("ReRAM_Title.txt", "w") as f:
    for i in clean_text:
        f.write(f"{str(i)}\n")

