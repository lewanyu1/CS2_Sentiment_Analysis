import pandas as pd

# 1. Read the data
data = pd.read_csv('/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis/2_data_warehouse/raw_data/tieba_result.csv')

# 2. Force the column to be numeric.
# 'coerce' turns any text (like 'reply_num') into NaN (Not a Number)
data['reply_num'] = pd.to_numeric(data['reply_num'], errors='coerce')

# 3. Sum the column (it ignores NaN by default)
num = data['reply_num'].sum()

print(int(num))