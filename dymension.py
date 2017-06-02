from datetime import datetime, timedelta
import pandas as pd


# TODO: Pull this from database
# TODO: Ensure this is sorted by eff_date

# Create dataframe based on *normalized* dimension data
norm_dims = [
    {'id': 1, 'entity': 'student', 'entity_id': 1111, 'attribute': 'major', 'value': 'MATH', 'eff_date': datetime(2015, 3, 1)},
    {'id': 2, 'entity': 'student', 'entity_id': 1111, 'attribute': 'major', 'value': 'ENGL', 'eff_date': datetime(2015, 3, 22)},
    {'id': 3, 'entity': 'student', 'entity_id': 1111, 'attribute': 'student_type', 'value': 'N', 'eff_date': datetime(2015, 3, 9)},
    {'id': 4, 'entity': 'student', 'entity_id': 1111, 'attribute': 'student_type', 'value': 'C', 'eff_date': datetime(2015, 4, 19)},
    {'id': 5, 'entity': 'student', 'entity_id': 1111, 'attribute': 'degree', 'value': 'BA', 'eff_date': datetime(2015, 3, 1)},
    {'id': 6, 'entity': 'student', 'entity_id': 1111, 'attribute': 'pell_recipient', 'value': 'Y', 'eff_date': datetime(2015, 2, 1)},
    {'id': 7, 'entity': 'student', 'entity_id': 2222, 'attribute': 'major', 'value': 'CSIS', 'eff_date': datetime(2015, 1, 1)}]

df = pd.DataFrame(norm_dims)

# Initialize variables
entity_ids = df.entity_id.unique()
df_den_list = []

# Loop over each entity and generate a dataframe with denormalized dimension
# data
for entity_id in entity_ids: 
    # Get a sub-dataframe based on individual entity and sort by eff date
    df_ent = df.loc[df['entity_id'] == entity_id]
    df_ent = df_ent.sort(['eff_date'], ascending=[True])

    # Get distinct eff-date to serve as the from-dates in the denormalized
    # dimension data
    from_dates = df_ent.eff_date.unique()

    # Initialize the denormalized-dimension dataframe
    df_den = pd.DataFrame({})

    df_den['from_date'] = from_dates

    # Use leading from-dates and subtract a millisecond to get to-dates; set
    # the last to-date to None to indicate the current dimension row
    df_den['to_date'] = df_den['from_date'].shift(-1) - timedelta(milliseconds=1)
    df_den.set_value(len(df_den) - 1, 'to_date', None)

    df_den['entity_id'] = entity_id

    # Loop over the entity's normalized dimensions and set each attribute-value
    # pair as a dataframe column and value
    for idx, row in df_ent.iterrows():
        df_den.ix[df_den.from_date >= row['eff_date'], row['attribute']] = row['value']

    df_den_list.append(df_den)

# Stitch it all together
final_df_den = pd.concat(df_den_list)

# TODO: Create destination table, grant needed permissions, index by id
# TODO: Populate destination table

# TODO: Separate script perhaps: assign dimension ids to fact tables based on
# entity ids and date ranges

print(final_df_den)