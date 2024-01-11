#https://github.com/fabiobatalha/crossrefapi

from crossref.restful import Works, Etiquette
import pandas as pd
import json
import jsonlines
from ast import literal_eval
from datetime import date
from pylatexenc.latex2text import LatexNodes2Text
from tqdm import tqdm

class Crossref:
    def __init__(self, keywords):
        self.mail = 'khyeon@postech.ac.kr'
        self.my_etiquette = Etiquette('Memory_Trend', '0.0.1', 'My Project URL', 'khyeon@postech.ac.kr')
        self.API = Works(etiquette=self.my_etiquette)
        self.ReRAM = pd.DataFrame(columns=['title','abstract','author','publisher','journal',"affiliation","funder",'date','is-referenced-by-count','reference','subject','type'])
        self.keyword_list = [ word.split(" ") for word in keywords ]
        self.document_list = ["journal-article","proceedings-article",
                                #"book-section",
                                #"monograph",
                                #"report",
                                #"book-track",
                                #"book-part",
                                #"other",
                                #"book",
                                #"journal-volume",
                                #"book-set",
                                #"reference-entry",
                                #"journal",
                                #"component",
                                #"book-chapter",
                                #"report-series",
                                #"proceedings",
                                #"standard",
                                #"reference-book",
                                #"posted-content",
                                #"journal-issue",
                                #"dissertation",
                                #"dataset",
                                #"book-series",
                                #"edited-book",
                                #"standard-series",
                                ]
        self.publication_year = ((1971,1,1),(2021,12,31))
        self.search_keyword_filename = "ReRAM_DB_Keyword.csv"
        self.filter_document_filename = "ReRAM_DB_Document.csv"
        self.filter_date_filename = "ReRAM_DB_Date.csv"
        self.filter_duplicate_filename = "ReRAM_DB_Duplicate.csv"

    def Article_search_keyword(self):
        for keyword in self.keyword_list:
            Total_query = []
            print(f"\nNow Searching for {keyword}\n")
            count = self.API.query(bibliographic=keyword[0]).count()
            for word in keyword:
                if count >= self.API.query(bibliographic=word).count():
                    min_word = word

            with tqdm(total= self.API.query(bibliographic=min_word).count()) as pbar:
                query = self.API.query(bibliographic=min_word)#.select("title","abstract","author","publisher","container-title","published-online","is-referenced-by-count","reference","subject","type","affiliation","funder")
                for q in query:
                    count = 0
                    try:
                        for word in keyword:
                            if q["title"][0].lower().find(word.lower()) != -1:
                                count+=1
                        if count == len(keyword):
                            Total_query.append(q)
                    except:
                        pass
                    pbar.update(1)

            with open("ReRAM_DB.jsonl",encoding="utf-8",mode="a") as f:
                for i in Total_query: f.write(json.dumps(i) + "\n")
            #self.Save_DF(Total_query,self.search_keyword_filename)

    def Json_to_csv(self):
        print("\nSaving DataFrame to CSV\n")
        df = self.ReRAM.copy()

        for idx,q in tqdm(enumerate(jsonlines.open("ReRAM_DB.jsonl"))):
            try:
                df.loc[idx, 'title'] = LatexNodes2Text().latex_to_text(str(q['title'][0]))
            except:
                pass
            try:
                df.loc[idx, 'abstract'] = q["abstract"]
            except:
                pass
            try:
                df.loc[idx, 'author'] = q["author"]
            except:
                pass
            try:
                df.loc[idx, 'publisher'] = q["publisher"]
            except:
                pass
            try:
                df.loc[idx, "journal"] = q["container-title"]
            except:
                pass
            try:
                affiliation = ""
                for i in q["affiliation"]:
                    affiliation += f"{i['name']},"
                if affiliation != "":
                    df.loc[idx,"affiliation"] = affiliation
            except:
                pass
            try:
                funder = ""
                for i in q["affiliation"]:
                    funder += f"{i['name']},"
                if funder != "":
                    df.loc[idx,"funder"] = funder
            except:
                pass
            try:
                df.loc[idx, 'date'] = q["published-online"]["date-parts"][0]
            except:
                pass
            try:
                df.loc[idx, 'is-referenced-by-count'] = q["is-referenced-by-count"]
            except:
                pass
            try:
                df.loc[idx, 'reference'] = q["reference"]
            except:
                pass
            try:
                df.loc[idx, 'subject'] = q["subject"]
            except:
                pass
            try:
                df.loc[idx, 'type'] = q["type"]
            except:
                pass

        df.to_csv("ReRAM_DB_Keyword.csv", index=False)
        print(f"\n{df.shape[0]} results in total")
        print("-----------------------------------------------------")

    def Article_filter_document(self):
        df = pd.read_csv(self.search_keyword_filename)
        df_new = self.ReRAM.copy()

        for idx in tqdm(range(len(df))):
            if df.loc[idx,"type"] in self.document_list:
                df_new.loc[len(df_new)] = df.loc[idx]

        df_new.to_csv(self.filter_document_filename, index=False)

        print(f"\n{df_new.shape[0]} results in total")
        print("-----------------------------------------------------")

    def Article_filter_date(self):
        df = pd.read_csv(self.filter_document_filename)
        df_new = self.ReRAM.copy()

        start_date = date(self.publication_year[0][0],self.publication_year[0][1],self.publication_year[0][2])
        end_date = date(self.publication_year[1][0],self.publication_year[1][1],self.publication_year[1][2])

        for idx in tqdm(range(len(df))):
            if str(df.loc[idx,"date"]) != "nan":
                pub_date=literal_eval(df.loc[idx,"date"])
                if len(pub_date) == 3:
                    article_date = date(pub_date[0],pub_date[1],pub_date[2])
                elif len(pub_date) == 2:
                    article_date = date(pub_date[0],pub_date[1],1)
                elif len(pub_date) == 1:
                    article_date = date(pub_date[0],1,1)

                if start_date <= article_date <= end_date:
                    df_new.loc[len(df_new)] = df.loc[idx]
                else:
                    print(article_date)

        df_new.to_csv(self.filter_date_filename, index=False)

        print(f"\n{df_new.shape[0]} results in total")
        print("-----------------------------------------------------")

    def Article_filter_duplicate(self):
        df = pd.read_csv(self.filter_date_filename)
        df_new = df.drop_duplicates(['title'], keep='first', ignore_index=True)

        df_new.to_csv(self.filter_duplicate_filename, index=False)

        print(f"\n{df_new.shape[0]} results in total")
        print("-----------------------------------------------------")

    def count_result(self):
        df = pd.read_csv(self.search_keyword_filename)
        print(f"\n Article search keyword: {len(df)} results in total")
        print("-----------------------------------------------------")

        df = pd.read_csv(self.filter_document_filename)
        print(f"\n Article filter document: {len(df)} results in total")
        print("-----------------------------------------------------")

        df = pd.read_csv(self.filter_date_filename)
        print(f"\n Article filter date: {len(df)} results in total")
        print("-----------------------------------------------------")

        df = pd.read_csv(self.filter_duplicate_filename)
        print(f"\n Article filter duplicate: {len(df)} results in total")
        print("-----------------------------------------------------")


'''2. 검색할 Keywords 지정'''
keywords = [
    "ReRAM",
    "RRAM",
    "OxRAM",
    "OxRRAM",
    "CBRAM",
    "Electrochemical Metallization Memory",
    "Valence Change Memory",
    "Resistive Switching",
    "Filament Switching",
    "Conductive Filament",
    "Conductive Bridge",
    "Oxygen Vacancies Filament"
    ]

#Crossref(keywords=keywords).Article_search_keyword()
Crossref(keywords=keywords).Json_to_csv()
Crossref(keywords=keywords).Article_filter_document()
Crossref(keywords=keywords).Article_filter_date()
Crossref(keywords=keywords).Article_filter_duplicate()
Crossref(keywords=keywords).count_result()
