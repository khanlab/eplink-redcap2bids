from redcap import Project
import pandas as pd
from io import StringIO

api_url = snakemake.params.api_url
api_key = snakemake.params.api_key
project = Project(api_url, api_key)

#select the particular events/forms we are interested in, to pre-load them..
data_dictionary = snakemake.params.data_dictionary

def get_dataframe_from_redcap(form_name,event_name):
  """ pulls as dataframe (note: the format_type='df' was not working due to some
  apparent incompatibility with the particular column names, so this approach
  of importing as CSV and then reading that as dataframe was needed..)"""

  csv = project.export_records(forms=[form_name],
                                     events=[event_name],
                                     raw_or_label='label',
                                     raw_or_label_headers='label',
                                     export_blank_for_gray_form_status=True,
                                     format_type='csv')

  df = pd.read_csv(StringIO(csv))

  return df

#preload all the data:
df_dict = {}

for event in data_dictionary.keys():
  df_dict[event] = { form:get_dataframe_from_redcap(form,event) for form in data_dictionary[event]}

def get_df_completed(df):
  """ simple wrapper for getting the completed rows of an instrument """
  return df[  df['Complete?'] == 'Complete' ].copy()

from math import isnan
from datetime import date, datetime

def get_age(birthyear, birthmonth, currdate_iso):
  """ complicated way to get age of each subject, but perhaps necessary """

  if isnan(birthyear):
    return float('nan')

  birthyear = int(birthyear)
  birthdate = datetime.strptime(f'{birthyear:d} {birthmonth}','%Y %B')
  currdate = datetime.fromisoformat(currdate_iso)
  age_years = (round((currdate-birthdate).days/365))
  return age_years


df = get_df_completed(df_dict['before_surgery_arm_1']['demographics'])

df_dict['before_surgery_arm_1']['demographics']['age_years'] = df.apply(lambda row: get_age(row["What is the participant's birth year?"],row["What is the participant's birth month?"],row["Date:"]),axis=1)
df['participant_id'] = 'sub-' + df['Subject ID'].str.split('_').str[1:].str.join('')


# use mapping to create new clean dataframe
df_clean = pd.DataFrame()

df_clean['participant_id'] = df['participant_id']

for arm in data_dictionary.keys():
  for instrument in data_dictionary[arm].keys():
    for oldcol,newcol in data_dictionary[arm][instrument].items():

      df_clean[newcol] = df_dict[arm][instrument][oldcol]

df_clean

#write to file
df_clean.to_csv(snakemake.output.tsv,index=False,sep='\t')
