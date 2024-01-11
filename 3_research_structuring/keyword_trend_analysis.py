import pandas as pd
from tqdm import tqdm
import ast

'''2. Plot 할 Keyword List 만들기'''
Topics = {
    "Structure-based":['resistive','switching','film','effect','thin','characteristic','switch','layer','behavior','structure','resistance','bipolar','pt','hfo2','property','mechanism','electrode','tio2','oxygen','zno',],
    "Neuromorphic":['base','rram','use','reram','memristor','high','low','array','cell','performance','memristive','current','network','power','voltage','model','neuromorphic','computing','self','neural',],
    "Performance-based":['memory','device','oxide','random','access','application','metal','conductive','filament','nonvolatile','non','volatile','flexible','graphene','state','organic','material','bridge','hybrid','perovskite',]
}
'''3. Keyword 개수 DB 불러오기'''
DB = pd.read_csv(f"/home1/khyeon/Researches/2_Text_mining/ReRAM_Trend/2_Publication_Year_Trend/ReRAM_Keyword_Freq_Year.csv",index_col="Keyword")
DB.index.name =  "year"

'''5. 각 연도에 대해서'''
for Topic in Topics.keys():
    df = DB.loc[Topics[Topic],:]
    for Key in Topics[Topic]:
        '''5-1. Category 내 각 Keywords 에 대해서'''
        df.loc[Key,:] = DB.loc[Key,:] # / DB.loc["Total Number",:]

    df = df[[str(x) for x in range(2005,2022)]]

    '''5-2. 행렬 전환'''
    df = df.transpose()
    df.index.name = "Year"

    '''6. 데이터 저장'''
    df.to_csv(f"{Topic}_year.csv")