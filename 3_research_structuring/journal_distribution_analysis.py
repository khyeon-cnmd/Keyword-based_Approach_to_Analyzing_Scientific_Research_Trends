import pandas as pd
from tqdm import tqdm
import ast

df = pd.read_csv("/home1/khyeon/Researches/2_Text_mining/ReRAM_Trend/1_Journal_Database2/ReRAM_DB_Final.csv")
df['journal'] = df['journal'].str.upper()
df['journal'] = df['journal'].str.replace(pat="'", repl='', regex=False)
df['journal'] = df['journal'].str.replace(pat="[", repl='', regex=False)
df['journal'] = df['journal'].str.replace(pat="]", repl='', regex=False)
df['journal'] = df['journal'].str.replace(pat=",", repl=' ', regex=False)

# 2. 연도별 journal 저장
with tqdm(total=len(df)) as pbar:


    df_journal = pd.DataFrame()
    count=0
    for index, row in df.iterrows():
        paper_year = int(ast.literal_eval(row['date'])[0])
        journal = row['journal']
        if paper_year in range(2006,2022):
            try:
                if str(df_journal.loc[journal,paper_year]) == "nan":
                    raise
                df_journal.loc[journal,paper_year] += 1
            except:
                df_journal.loc[journal,paper_year] = 1
            try:
                if str(df_journal.loc[journal,"Total"]) == "nan":
                    raise
                df_journal.loc[journal,"Total"] += 1
            except:
                df_journal.loc[journal,"Total"] = 1
        pbar.update(1)

# 3. 저장
df_journal = df_journal[[2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,'Total']]
# if publisher contain year, remov
df_journal.index = df_journal.index.str.replace(pat="20\d\d", repl='', regex=True)

df_journal2 = df_journal.copy()
journals = []
for i in range(2006,2022):
    df_journal2[i] = df_journal[i]/df_journal[i].sum()
    # make rank on the column i

df_journal2.to_csv("total.csv")
