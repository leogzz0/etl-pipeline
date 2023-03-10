#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leogzz0
"""

from sqlalchemy import create_engine
import pyodbc
import pandas as pd
import config.email as eml
import os

#get password from enviroment var
pwd = os.environ['leonardo3223']
uid = os.environ['UFC1993l//']
server = 'localhost'
db= 'AdventureWorks'
port = '5432'
dire = r"../Desktop/etl-pipeline/data"
to = 'leogzz0@hotmail.com'

def extract():
    try:
        #starting directory
        directory = dire 
        #iterate over files in the directory
        for filename in os.listdir(directory):
            #get filename without extension
            file_wo_text = os.path.splitext(filename)[0]
            #only process excel files
            if filename.endswith('.xlxs'):
                f = os.path.join(directory, filename)
                #checking if it is a file
                if os.path.isfile(f):
                    df = pd.read_excel(f)
                    #call to load
                    load(df, file_wo_text)
    except Exception as e:
        eml.send_mail(to, 'File Upload, Data extract error: ', f'Data extract error: File location {dire}' + str (e))
        print("Data extract error: " + str(e))

#load data to postgres
def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{db}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... ')
        # save df to postgres
        df.to_sql(f"stg_{tbl}", engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # add elapsed time to final print out
        print("Data imported successful")
        eml.send_mail(to, "File Uploaded, Data load successful: ", "Data load notification for : " + f"stg_{tbl}")
    except Exception as e:
        eml.send_mail(to, "File Upload Data load error: ", f"Data extract error: File location {dir}"  + str(e))
        print("Data load error: " + str(e))

try:
    #call extract function
    df = extract()
except Exception as e:
    eml.send_mail(to, "File Upload, Data extract error: ", f"Function call to file mapping, Data extract error: File location {dir}" + str(e))
    print("Error while extracting data: " + str(e))

"""
 *  
 *     ("`-''-/").___..--''"`-._
 *      `6_ 6  )   `-.  (     ).`-.__.`)
 *      (_Y_.)'  ._   )  `._ `. ``-..-'
 *    _..`--'_..-_/  /--'_.' ,'
 *   (il),-''  (li),'  ((!.-'      @leogzz0
 *      
"""