"""
benefits.highlights & salary.salaries in the original data set
has a primary key other than jobId.
This script finds the related jobId and replaces the primary key to better fit our model
"""
import pandas as pd
import csv

highlight_fieldnames = ['gaTrackerData.jobId', 'icon', 'name', 'highlightPhrase']
salary_fieldnames = ['gaTrackerData.jobId', 'jobTitle', 'payPeriod', 'payPercentile50', 'payPercentile10', 'payPercentile90']

def cast_to_int(df, columns):
    """
    cast all values from float to int and rename jobId column
    """
    df = df.dropna()
    df = df.rename(columns={'gaTrackerData.jobId.long': 'gaTrackerData.jobId'})
    for c in columns:
        df[c] = pd.to_numeric(df[c], downcast='signed')
    return df

def get_jobId(id, rel):
    return rel.loc[rel['salary.salaries'] == id]

def get_source_row(id, rel):
    a = rel.loc[rel['id'] == id]
    return a

def execute(isHighlights):
    if isHighlights:
        csv = pd.read_csv('UK_highlights.csv')
        columns = ['gaTrackerData.jobId', 'benefits.highlights']
        output_csv = 'UK_benefits_highlights.csv'
        details_csv = 'glassdoor_benefits_highlights.csv'
    else:
        csv = pd.read_csv('UK_salaries.csv')
        columns = ['gaTrackerData.jobId', 'salary.salaries']
        output_csv = 'UK_salary_salaries.csv'
        details_csv = 'glassdoor_salary_salaries.csv'

    og_df = cast_to_int(csv, columns)
    details_df = pd.read_csv(details_csv)
    details_df = details_df.dropna()

    rows = pd.DataFrame(columns=details_df.columns)

    for id in details_df['id']:
        try:
            jobId = get_jobId(id, og_df).iloc[0]['gaTrackerData.jobId']
        except:
            # highlights or salary info not found
            continue

        dest = get_source_row(id, details_df)

        tot_src_rows, cols = dest.shape
        dest.loc[:, ('id')] = [jobId for i in range(0, tot_src_rows)]

        dest.to_csv(output_csv, mode='a', header=False)



if __name__=="__main__":
    execute(False)
