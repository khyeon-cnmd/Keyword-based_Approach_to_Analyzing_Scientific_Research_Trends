import pandas as pd
from tqdm import tqdm

'''1. 연도 설정'''
YStart=1971
Yend=2022

'''2. Page Rank 데이터 불러오기'''
PR = pd.read_csv(f"{YStart}-{Yend}_PR.csv")
PR = PR.sort_values(by=["pageranks"],ascending=False)

'''3. Keyword 개수 DB 불러오기'''
DB = pd.read_csv(f"../2_Publication_Year_Trend/ReRAM_Keyword_Freq_Year.csv",index_col="Keyword")
DB = DB[[str(x) for x in range(YStart,Yend)]]

'''4. 모든 Keyword 에 대해서'''
df = pd.DataFrame()
df.index.name = "Keyword"
Int = 0
for Index,Row in tqdm(PR.iterrows()):
    '''4-1. Keyword 이름 불러오기'''
    try:
        Id = Row["Id"].replace("\t","\\t").replace("\n","\\n").replace("\a","\\a")
    except:
        pass
    if Id == "nan":
        Id = "null"

    '''4-2. Page Rank 점수 저장'''
    df.loc[Id,"PR"] = Row["pageranks"]

    '''4-3. 해당 Keyword 의 총 개수 및 전체 Keyword 개수 저장'''
    df.loc[Id,"Num"] = DB.sum(axis=1)[Id]
    Int = Int + DB.sum(axis=1)[Id]
    df.loc[Id,"Total"] = DB.sum(axis=1)["Total Number"]
    df.loc[Id,"Ratio"] = Int / DB.sum(axis=1)["Total Number"]

df.to_csv(f"{YStart}-{Yend}_Distribution.csv")