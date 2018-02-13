import pandas as pd

col_header = ['CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE', 'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID',
            'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID']
ind_d = pd.read_csv('itcont.txt', sep = "|", names = col_header)
ind_d1 = ind_d[['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID']]
n = int(pd.read_csv('percentile'))

index_set = [isinstance(ind_d1["OTHER_ID"][i],float) for i in range(len(ind_d1.OTHER_ID)) ]
df_index_other_id = pd.DataFrame({'index_set': index_set})
ind_d1.insert(loc=6, column='index_set', value=df_index_other_id, allow_duplicates = True)
#Preserve all entries with NaN in OTHER_ID column
ind_d2 = ind_d1[ind_d1['index_set'] == True]
#Get the first five digits of ZIP_CODE
ind_d2['ZIP_CODE'] = ind_d2['ZIP_CODE'].apply(lambda x: str(x))
ind_d2['ZIP_CODE'] = ind_d2['ZIP_CODE'].astype(str).str[:5]
#Find repeated entries based on CMTE_ID and ZIP_CODE
ind_d3 = pd.concat(g for _, g in ind_d2.groupby(['CMTE_ID', 'ZIP_CODE']) if len(g) > 1)
ind_d4 = ind_d3.sort_values(by='NAME', axis=0)
#Drop all invalid names and store into a new dataframe ind_d5
ind_d4['NAME'] = ind_d4['NAME'].apply(lambda x: str(x))
ind_d5 = ind_d4[ind_d4['NAME'] != 'nan']
ind_d5['TRANSACTION_DT'] = ind_d5['TRANSACTION_DT'].astype(str).str[-4:]
ind_d5.drop(['OTHER_ID', 'index_set'], axis=1, inplace=True)
