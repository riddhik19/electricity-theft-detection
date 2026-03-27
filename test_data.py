import pandas as pd
import numpy as np
import gc

# Load data
daily = pd.read_csv("daily_dataset.csv", usecols=['LCLid', 'day', 'energy_sum', 'energy_count'])
print('Loaded daily data shape:', daily.shape)

# Convert day to datetime
daily['day'] = pd.to_datetime(daily['day'])

# Check date range
print('Date range:', daily['day'].min(), 'to', daily['day'].max())

# Filter 2013
final_2013 = daily[daily['day'].dt.year == 2013].copy()
print('2013 data shape:', final_2013.shape)
print('Unique households in 2013:', final_2013['LCLid'].nunique())

# Check valid_ids - households with > 250 data points
valid_ids = final_2013.groupby("LCLid").size()
print('Total households:', len(valid_ids))
print('Households with > 250 days:', (valid_ids > 250).sum())
valid_ids = valid_ids[valid_ids > 250].index
print('Filtered valid_ids count:', len(valid_ids))

# Check agg_features
agg_features = final_2013.groupby("LCLid")['energy_sum'].agg([
    'mean', 'std', 'max', 'min', 
    ('zero_days', lambda x: (x == 0).sum())
]).reset_index()
print('agg_features shape:', agg_features.shape)
print('Columns:', agg_features.columns.tolist())
print('agg_features head:')
print(agg_features.head())

