import re, os, requests, nltk
import pdfplumber

import pandas as pd

stopword = ["WHAT'S NEW IN TIRES","HAT'S NEW IN TIRES","FINANCE","INANCE", "RELATED MATTERS", "VEHICLE INDUSTRY NEWS"]


def Smithers_Report_Translator(pFilepath) :
    filename = pFilepath[7:-4]
    df = pd.DataFrame(columns=['title','main'])
    pdf = pdfplumber.open(pFilepath)
    page = pdf.pages

    for i in range(len(page)):
        text = page[i].extract_text()
        text = text.replace(')\n', ')\n\n')
        if i != 0 :
            text = re.split('Page [0-9] of [0-9]', text)
            text_para = text[1].split('\n\n')
        else : 
            text = re.split('Vol. \d+, No. \d+\S+', text)
            text_para = text[1].split('\n\n')

        for j in range(len(text_para)) :
            text_list = str(text_para[j]).split('\n')
            
            for sw in stopword:
                if sw in text_list:
                    print('>>remove: ' + sw)
                    text_list.remove(sw)
                else:
                    pass
                
                if text_list[0] == "" :
                    text_main = str(text_list[2:]).replace("', '", " ")
                    text_main = str(text_main[:]).replace("']", "")
                    text_main = str(text_main[:]).replace("['", "")
                    text_df = pd.DataFrame([{'title' : text_list[1], 'main' : text_main}])
                else :
                    text_main = str(text_list[1:]).replace("', '", " ")
                    text_main = str(text_main[:]).replace("']", "")
                    text_main = str(text_main[:]).replace("['", "")
                    text_df = pd.DataFrame([{'title' : text_list[0], 'main' : text_main}])
                               
                # text_dict = {'title' : text_list[0], 'main' : text_main[1:]}
            # df = df.append(text_dict, ignore_index=True)
            df = pd.concat([df, text_df]).reset_index(drop=True)
    df.to_csv("{}.csv".format(filename),encoding='utf-8-sig')

filepath = input("파일경로를 붙여넣어주세요. ex)'D:\dev\git\readpdf\file\The Smithers Report Oct 7 2021.pdf' :")
filepath = filepath.replace("\\", '/')

Smithers_Report_Translator(pFilepath = filepath)