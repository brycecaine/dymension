from datetime import datetime, timedelta
import pandas as pd


# Ensure this is sorted by eff_date
norm_dims = [
    {'id': 1, 'entity': 'student', 'entity_id': 1111, 'attribute': 'major', 'value': 'MATH', 'eff_date': datetime(2015, 3, 1)},
    {'id': 2, 'entity': 'student', 'entity_id': 1111, 'attribute': 'major', 'value': 'ENGL', 'eff_date': datetime(2015, 3, 22)},
    {'id': 3, 'entity': 'student', 'entity_id': 1111, 'attribute': 'student_type', 'value': 'N', 'eff_date': datetime(2015, 3, 9)},
    {'id': 4, 'entity': 'student', 'entity_id': 1111, 'attribute': 'student_type', 'value': 'C', 'eff_date': datetime(2015, 4, 19)},
    {'id': 5, 'entity': 'student', 'entity_id': 1111, 'attribute': 'degree', 'value': 'BA', 'eff_date': datetime(2015, 3, 1)},
    {'id': 6, 'entity': 'student', 'entity_id': 1111, 'attribute': 'pell_recipient', 'value': 'Y', 'eff_date': datetime(2015, 2, 1)}]

denorm_dims = []

df = pd.DataFrame(norm_dims)
df = df.sort(['eff_date'], ascending=[True])

from_dates = df.eff_date.unique()
to_dates = from_dates[1:]

df_2 = pd.DataFrame({})
df_2['from_date'] = from_dates
df_2['to_date'] = df_2['from_date'].shift(-1) - timedelta(milliseconds=1)
df_2.set_value(len(df_2) - 1, 'to_date', None)
df_2['entity_id'] = 1111

for norm_dim in norm_dims:
    df_2.ix[df_2.from_date >= norm_dim['eff_date'], norm_dim['attribute']] = norm_dim['value']

print(df_2)