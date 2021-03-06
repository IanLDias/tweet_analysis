import pandas as pd
df = pd.read_excel('data_labeling/label_data_ian.xlsx', engine='openpyxl')
print(df['label'].value_counts())