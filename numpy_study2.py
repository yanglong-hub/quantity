import numpy as np
import pandas as pd

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6,4)),index=dates, columns=['A','B','C','D'])
#print(df['A'],df.A)
#print(df[0:3])
#select by label:loc
#print(df['20130102':'20130104'])
#print(df.loc['20130102'])
#print(df.loc['20130102',['A','B']])

#select by position:iloc
#print(df.iloc[3:5,1:3])
#print(df.iloc[[1,3,5],1:3])

#mixed selection:ix 废弃0.20
#print(df.iloc[:3,['A','C']])
#print(df)
#print(df[df.A > 8])

#df.iloc[2,2] = 1111
#df.loc['20130101','B'] = 2222
#df.B[df.A >4] = 0
#df['F'] = np.nan
#df['E'] = pd.Series([1,2,3,4,5,6],index=pd.date_range('20130101', periods=6))
#print(df)

#df.iloc[0,1] = np.nan
#df.iloc[1,2] = np.nan
#print(df.dropna(axis=0, how='any')) # how={'any','all'}
#print(df.fillna(value=0))
#print(np.any(df.isnull()) == True)

#data  = pd.read_csv('000300.SH.csv')
#print(data)
#data.to_pickle('00030.pickle')

#concatenating