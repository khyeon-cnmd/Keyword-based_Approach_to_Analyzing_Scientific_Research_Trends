import pandas as pd
from tqdm import tqdm

class Integrated_DB:
    def __init__(self):
        self.CrossRef = pd.read_csv("1_CrossRef/ReRAM_DB_Duplicate.csv")
        self.CrossRef['title'] = self.CrossRef['title'].str.lower()
        print(len(self.CrossRef))
        self.WOB = pd.read_csv("2_WebOfScience/ReRAM_DB_Duplicate.csv")
        self.WOB['title'] = self.WOB['title'].str.lower()
        print(len(self.WOB))
        self.Prev_DB = pd.read_csv("../1_Journal_Database/ReRAM_DB_Stopwords.csv")
        print(len(self.Prev_DB))

    def DB_Duplication(self):
        # 1. 특수 문자 전처리
        for idx, row in self.CrossRef.iterrows():
            self.CrossRef.loc[idx, 'title'] = row['title'].replace("−", "-").replace("—", "-").replace("–", "-").replace("‐", "-").replace("≤", "<=").replace("<sub>", "").replace("</sub>", "").replace("<sup>", "").replace("</sup>", "").replace("<i>", "").replace("</i>", "").replace("<italic>", "").replace("</italic>", "").replace("<font>", "").replace("</font>", "").replace("hbox", "").replace("ₓ", "x").replace("₂", "2").replace("δ", "delta").replace("α", "alpha").replace("κ", "kappa").replace("γ", "gamma").replace("β", "beta")

        # 2. 제목 소문자화 후 중복 제거
        #Drop = []
        #for idx, row in self.CrossRef.iterrows():
        #    idx2 = self.CrossRef[self.WOB['title'] == row['title']].index.to_list()
        #    Drop+=idx2
        #Drop = list(set(Drop))
        #print(f"\n Drop Indexes: {Drop}")
        #self.CrossRef = self.CrossRef.drop(index=Drop)
        #self.CrossRef.reset_index(drop=True, inplace=True)
#
        print(f"\nDB Duplication 1: {len(self.CrossRef) + len(self.WOB)} results in total")
        print("-----------------------------------------------------")

    def DB_Duplication_2(self):
        Drop = []
        Check = []
        for index, row in self.CrossRef.iterrows():
            CrossRef_List = set(row['title'].split(" "))

            for index2, row2 in self.WOB.iterrows():
                WOB_List = set(row2['title'].split(" "))
                Lset = list(CrossRef_List - WOB_List)
                Rset = list(WOB_List - CrossRef_List)

                if len(Lset) == 1 and len(Rset) == 1:

                    if Lset + Rset == ['+','plus']:
                        Drop.append(index)
                        break

                    Llet = set(list(Lset[0]))
                    Rlet = set(list(Rset[0]))
                    Lset = list(Llet - Rlet)
                    Rset = list(Rlet - Llet)

                    if len(Lset) == 0 or len(Rset) == 0:
                        Drop.append(index)
                        break

                    else:
                        Check.append((index,index2,CrossRef_List - WOB_List,WOB_List - CrossRef_List))
                        break

        print("===============CHECK================")

        for idx in Check:
            print(f"{idx[0]}:{self.CrossRef.loc[idx[0],'title']}\n{idx[1]}:{self.WOB.loc[idx[1],'title']}\n{idx[2]}\t{idx[3]}\n")
            YN = input(f"Do we delete the {idx[0]} row? (y=Enter/n)")
            if YN == "y" or YN == "":
                Drop.append(idx[0])

        print(f"\n Drop Indexes: {Drop}")
        self.CrossRef = self.CrossRef.drop(index=Drop)
        self.CrossRef.reset_index(drop=True, inplace=True)

        print(f"\nDB Duplication 2: {len(self.CrossRef) + len(self.WOB)} results in total")
        print("-----------------------------------------------------")

    def DB_Integration(self):
        self.df_total=pd.concat([self.CrossRef,self.WOB],ignore_index=True)
        self.df_total.reset_index(drop=True, inplace=True)
        print(self.df_total)
#
        self.df_total.to_csv("ReRAM_DB_Integrated.csv", index=False)
        print(f"\nDB Integration: {len(self.df_total)} results in total")
        print("-----------------------------------------------------")

    def DB_Stopwords(self):
        Delete = [
            "mml", #추출시 오류가 존재
            ";sub", #추출시 오류가 존재
            "gt;" #추출시 오류가 존재
        ]
        '''2. Keyword 의 포함 여부를 통해서 논문 선별'''
        Dead = []
        for word in Delete:
            for index, row in self.df_total.iterrows():
                if str(row['title']).lower().find(word) != -1:
                    Dead.append(index)

        '''3. Dead 중 중복 index 제거'''
        Dead = list(set(Dead))
        df_total = self.df_total.drop(index=Dead)

        df_total.to_csv("ReRAM_DB_Stopwords.csv", index=False)
        print(f"\nDB Stopwords: {len(df_total)} results in total")
        print("-----------------------------------------------------")

    def DB_Compare(self):
        delete = [x for x in range(len(self.df_total))]
        pre_exists = []
        for idx, row in tqdm(self.df_total.iterrows()):
            if (self.Prev_DB["title"] == row["title"]).any():
                pre_exists.append(idx)
        delete = [x for x in delete if x not in pre_exists]
        self.df_total = self.df_total.drop(delete).reset_index(drop=True)

        self.df_total = self.df_total.drop_duplicates(["title"])
        self.df_total.reset_index(drop=True, inplace=True)
        print(len(self.df_total))
        self.df_total.to_csv("ReRAM_DB_Final.csv")

#Int = Integrated_DB()
#Int.DB_Duplication()
##Int.DB_Duplication_2()
#Int.DB_Integration()
##Int.DB_Stopwords()
#Int.DB_Compare()

df = pd.read_csv("ReRAM_DB_Final.csv")
print(len(df.drop_duplicates(["title"])))
print(len(df))