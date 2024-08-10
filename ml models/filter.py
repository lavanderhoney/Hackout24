import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# Load the CSV file into a DataFrame
df = pd.read_csv('yield_df.csv')

# Filter the DataFrame to keep only rows where 'Area' is 'India'
df_filtered = df[df['Area'] == 'India'].copy()

print(df_filtered)
df_filtered.drop_duplicates(inplace=True)

def isStr(obj):
    try:
        float(obj)
        return False
    except:
        return True
    
to_drop = df[df['average_rain_fall_mm_per_year'].apply(isStr)].index
df_filtered = df_filtered.drop(to_drop)

# print(df_filtered)


# sns.countplot(y=df_filtered['Item'])
# plt.show()
# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv('yield_ind.csv', index=False)
