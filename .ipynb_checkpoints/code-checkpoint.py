import hashlib 
import pandas as pd
from pandas_profiling import ProfileReport

df_boxoffice = pd.read_csv('./data/boxoffice.csv')
df_metadata = pd.read_csv('./data/movies_metadata.csv.zip')
#simple EDA for boxoffice dataset
eda_boxoffice = ProfileReport(df_boxoffice)
eda_boxoffice.to_file(output_file='./eda/boxoffice_eda.html')
#simple EDA for metadata dataset
eda_metadata = ProfileReport(df_metadata)
eda_metadata.to_file(output_file='./eda/metadata_eda.html')
#small transformations for boxoffice
df_boxoffice['id'] = df_boxoffice.apply(lambda x: hashlib.md5(x['title'].replace(" ", "").lower().encode()+str(x['year']).encode()).hexdigest() , axis=1)
del df_boxoffice['rank']
del df_boxoffice['studio']
#some transformations for the metadata dataset
df_metadata.dropna(subset = ['release_date', 'title'], inplace=True)
df_metadata['budget'] = pd.to_numeric(df_metadata['budget'])
df_metadata['year'] = df_metadata.apply(lambda x: str(x['release_date'])[0:4], axis=1)
df_metadata['id'] = df_metadata.apply(lambda x: hashlib.md5(x['title'].replace(" ", "").lower().encode()+str(x['year']).encode()).hexdigest() , axis=1)
df_metadata = (df_metadata.loc[df_metadata['budget'] > 0][['id','title','year','budget','vote_average','vote_count']]).copy()
#merged dataset
df = df_metadata.join(df_boxoffice.set_index('id'), on='id', lsuffix='_metadata', rsuffix='_boxoffice')
df.dropna(subset = ['title_boxoffice'], inplace=True)
df.drop_duplicates(subset=['id'], inplace=True)
#automatic EDA with correlations between vars calculated on the merged dataset 
eda_df = ProfileReport(df)
eda_df.to_file(output_file='./eda/df_eda.html')