import pandas as pd
from tqdm import tqdm

'''1. 연도 설정'''
YStart=1971
Yend=2022

'''2. Page Rank 데이터 불러오기'''
PR = pd.read_csv(f"{YStart}-{Yend}_PR_MOD.csv")
PR = PR.sort_values(by=["pageranks"],ascending=False)

'''3. Keyword 개수 DB 불러오기'''
DB = pd.read_csv(f"../2_Publication_Year_Trend/ReRAM_Keyword_Freq_Year.csv",index_col="Keyword")
DB = DB[[str(x) for x in range(YStart,Yend)]]

'''4. Modularity Class 에 따라서 Keyword 를 분리'''
Keyword_Criteria = 514
Modularity = {}
for Index,Row in PR.iterrows():
    '''4-1. Keyword 이름 불러오기'''
    try:
        Id = Row["Id"].replace("\t","\\t").replace("\n","\\n").replace("\a","\\a")
    except:
        pass
    if Id == "nan":
        Id = "null"

    '''4-2. 각 Modularity_class 에 Keyword 이름 List 로 저장'''
    if Row["modularity_class"] not in Modularity.keys():
        Modularity[Row["modularity_class"]] = []
    Modularity[Row["modularity_class"]].append(Id)

    if Index +1 == Keyword_Criteria:
        break

'''5. 각 연도에 대해서'''
df = pd.DataFrame()
for Year in range(YStart,Yend):

    '''5-1. 각 Modularity Class 에 대해서'''
    for Class in Modularity.keys():

        '''5-2. Class 내 모든 Keywords 의 총 개수 합을 구함'''
        Class_Sum = 0
        for Key in Modularity[Class]:
            Class_Sum = Class_Sum + DB.loc[Key,str(Year)]

        '''5-3. 각 Class 에 기입'''
        df.loc[Year,Class] = Class_Sum

    '''5-4. 총 Keyword 개수를 기입'''
    df.loc[Year,"Total"] = DB.loc["Total Number",str(Year)]

'''6. 데이터 저장'''
df.to_csv(f"Category_year.csv")
