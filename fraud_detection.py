##Fraud detection in subsidy applications in the Netherlands

##Comparing chamber of commerce (KVK) numbers

import pandas as pd
import numpy as np

#Create a dataframe called dff by reading 'faillissement_database.xlsx'.
dff=pd.read_excel('faillissement_database.xlsx')

#Create a dataframe called df by reading 'government_database.xlsx'.
df=pd.read_excel('government_database.xlsx')

#Add a column to the df dataframe called "KVK number in fai. database"
#and give the value "yes" if the number matches otherwise "None".
df["KVK number in fai. database"] = list(map(lambda x: "yes" if x else "None", np.in1d(df.ORG_KVK, dff.ORG_KVK)))

##Check multiple submissions

#Check same KVK number in multiple applications
df['kvk_dubble']=None
df.loc[df.duplicated('ORG_KVK', keep=False), 'kvk_dubble']='yes'

#Check same bank number in multiple applications
df['IBAN_dubble']=None
df.loc[df.duplicated('ORG_IBAN', keep=False), 'IBAN_dubble']='yes'

#Check same PO box / address in multiple applications
df['Adres_combined'] = df['ORG_STREETNAME']+' '+df['ORG_HOUSENUMBER']+' '+df['ORG_ZIPCODE']
df['adres_dubble']=None
df.loc[df.duplicated('Adres_combined', keep=False),'adres_dubble']='yes'

#Check foreign bank number in the applications
df['ORG_IBAN'].astype('str')
df['no NL Banknummer']=None
import re
for i in range (0, len(df.index)):
    substring='NL'
    mainstring=df['ORG_IBAN'][i] 
    if re.search(substring, mainstring) is None:
        df['no NL Banknummer'][i]='yes' 

#Check same e-mail adress in multiple applications
df['email_dubble']=None
df.loc[df.duplicated('CP_EMAIL', keep=False), 'email_dubble']='yes'

#Check same signatory in multiple applications
df['CP_NAME']=df['CP_FIRST NAME']+' '+df['CP_LAST NAME']
df['contact_dubble']=None
df.loc[df.duplicated('CP_NAME', keep=False), 'contact_dubble']='yes'

#Check private e-mail domains (Hotmail.com, gmail.com)
domain_list=['hotmail', 'kpnmail', 'kpnplanet' , 'casema', 'caiway',
 'gmail', 'ziggo', 'ADSL', 'online', 'stipte', 'tele2', 'telfort',
 'vodafone' 'solcon','youfone', 'live', 'outlook','Tele2', 'DELTA',
 'Budget', 'protonmail', 'googlemail', 'yahoo','yahoomail','t-mobile',
 'kabelnoord', 'XS4ALL']
df["Email not company domain"] = list(map(lambda x: "yes" if x else 'None', (df['res'].isin(domain_list))))

#Check same telephone number in multiple applications
df['tele_dubble']=None
df.loc[df.duplicated('CP_PHONE', keep=False), 'tele_dubble']='yes'

##Summerizing results

#Creating a summerzing dataframe for KVK numbers
df_KVK=df[[ 'ORG_KVK','REFERENCE','ORG_NAAM']]
df_KVK1 = df_KVK[df_KVK.duplicated(subset=['ORG_KVK'], keep=False)].sort_values(by='ORG_KVK', ascending=False).reset_index(drop=True)
tab_KVK = pd.pivot_table(df_KVK1, index=['ORG_KVK',"REFERENCE","ORG_NAME"])

#Creating a summerzing dataframe for IBAN numbers
df_IBAN=df[[ 'ORG_IBAN','REFERENCE','ORG_NAME']] 
df_IBAN1 = df_IBAN[df_IBAN.duplicated(subset=['ORG_IBAN'], keep=False)].sort_values(by='ORG_IBAN', ascending=False).reset_index(drop=True) 
tab_IBAN = pd.pivot_table(df_IBAN1, index=['ORG_IBAN',"REFERENCE", "ORG_NAME"])

#Creating a summerzing dataframe for e-mail addresses
df_EMAIL=df[[ 'CP_EMAIL','REFERENCE','ORG_NAME']]
df_EMAIL1 = df_EMAIL[df_EMAIL.duplicated(subset=['CP_EMAIL'], keep=False)].sort_values(by='CP_EMAIL', ascending=False).reset_index(drop=True)
tab_EMAIL = pd.pivot_table(df_EMAIL1, index=['CP_EMAIL','REFERENCE','ORG_NAME'])

#Creating a summerizing dataframe for telefone numbers
df_TELEFOON=df[[ 'CP_PHONE','REFERENCE','ORG_NAME']]
df_TELEFOON1 = df_TELEFOON[df_TELEFOON.duplicated(subset=['CP_PHONE'],keep=False)].sort_values(by='CP_PHONE', ascending=False).reset_index(drop=True)
tab_TELEFOON = pd.pivot_table(df_TELEFOON1, index=['CP_PHONE','REFERENCE','ORG_NAME'])

#Creating a summerizing dataframe for same signatory
df_NAAM=df[[ 'CP_NAME','REFERENCE','ORG_NAME']]
df_NAAM1 = df_NAAM[df_NAAM.duplicated(subset=['CP_NAME'], keep=False)].sort_values(by='CP_NAME', ascending=False).reset_index(drop=True)
tab_NAAM = pd.pivot_table(df_NAAM1, index=['CP_NAME','REFERENCE','ORG_NAME'])

#Creating a summerizing dataframe for same address
df_Adres=df[[ 'Adres_combined','REFERENCE','ORG_NAME']]
df_Adres1 = df_Adres[df_Adres.duplicated(subset=['Adres_combined'], keep=False)].sort_values(by='Adres_combined', ascending=False).reset_index(drop=True)
tab_Adres = pd.pivot_table(df_Adres1, index=['Adres_combined','REFERENCE','ORG_NAME'])

##Printing results
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter') 
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0,startcol=0)
    writer.save()

dfs = [df, tab_KVK, tab_IBAN, tab_EMAIL, tab_TELEFOON, tab_NAAM, tab_Adres]
sheets = ['Bron','KVK','IBAN','Email','telefoon','Contactpersoon','Adres']

dfs_tabs(dfs, sheets, 'multi-controle.xlsx')



