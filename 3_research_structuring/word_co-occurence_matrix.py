import pandas as pd
import gc
#ignore warning including name of "PerformanceWarning"

from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

'''1. 앞서 Tokenized 된 제목에 대해서 Space 를 기준으로 단어 분리'''
cv = CountVectorizer(ngram_range=(1,1), stop_words = None, tokenizer=lambda x: x.split(' '))

Decades=[(1971,2022)]

for YStart, Yend in Decades:
    # open title strings
    all_text=[]
    with open("/home1/khyeon/Researches/2_Text_mining/ReRAM_Trend/1_Journal_Database2/ReRAM_Title.txt",'r') as f:
        for i in f.readlines():
            Title,Date=i.strip().split("\t")
            if int(Date) in range(YStart,Yend):
                all_text.append(Title)

    # matrix of token counts
    df = pd.DataFrame()
    for idx, text in tqdm(enumerate(all_text)):
        print(text)
        X = cv.fit_transform([text])
        text = cv.get_feature_names()
        for i in range(len(text)):
            for j in range(i+1,len(text)):
                if text[i] in df.columns and text[j] in df.columns:
                    df.loc[text[i],text[j]]+=1
                    df.loc[text[j],text[i]]+=1
                elif text[i] in df.columns:
                    df.loc[text[i],text[j]]=1
                    df.loc[text[j],text[i]]=1
                elif text[j] in df.columns:
                    df.loc[text[j],text[i]]=1
                    df.loc[text[i],text[j]]=1
                else:
                    df.loc[text[i],text[j]]=1
                    df.loc[text[j],text[i]]=1
        if idx == 100:
            break
    
    

    #sort columns and rows by alphabet
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.columns), axis=0)
    print(df)

    # CV
    X = cv.fit_transform(all_text[0:101])
    Xc = (X.T * X) # matrix manipulation
    Xc.setdiag(0) # set the diagonals to be zeroes as it's pointless to be 1
    names = cv.get_feature_names() # This are the entity names (i.e. keywords)
    df2 = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
    #sort columns and rows by alphabet
    df2 = df2.reindex(sorted(df.columns), axis=1)
    df2 = df2.reindex(sorted(df.columns), axis=0)
    print(df2)


    df.to_csv(f"{YStart}-{Yend}_no_scikit.csv", sep = ',')


    df.to_csv(f"{YStart}-{Yend}_test.csv", sep = ',')



