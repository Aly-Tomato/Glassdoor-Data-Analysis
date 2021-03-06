"""
benefits.highlights & salary.salaries in the original data set
has a primary key other than jobId.
This script finds the related jobId and replaces the primary key to better fit our model
"""
import pandas as pd
import csv


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

def filter_highlights_columnns():
    highlight_OG_fieldnames = ['id', 'benefits.highlights.val.icon', 'benefits.highlights.val.name', 'benefits.highlights.val.highlightPhrase']
    df = pd.read_csv('../raw_data/formatted_UK_benefits_highlights.csv')
    df = df.rename(columns={'id': 'gaTrackerData.jobId',
                       'benefits.highlights.val.icon': 'icon',
                       'benefits.highlights.val.name': 'name',
                       'benefits.highlights.val.highlightPhrase': 'highlightsPhrase'
    })
    del df['benefits.highlights.val.commentCount']
    df.to_csv('../raw_data/formatted_UK_benefits_highlights.csv')

def filter_salary_columns():
    salary_fieldnames = ['gaTrackerData.jobId', 'jobTitle', 'payPeriod', 'payPercentile50', 'payPercentile10', 'payPercentile90']
    df = pd.read_csv('../raw_data/formatted_UK_salary_salaries.csv')
    df = df.rename(columns={'id': 'gaTrackerData.jobId',
                            'salary.salaries.val.jobTitle': 'jobTitle',
                            'salary.salaries.val.payPeriod': 'payPeriod',
                            'salary.salaries.val.salaryPercentileMap.payPercentile50': 'payPercentile50',
                            'salary.salaries.val.salaryPercentileMap.payPercentile10': 'payPercentile10',
                            'salary.salaries.val.salaryPercentileMap.payPercentile90': 'payPercentile90',
                            })
    del df['index']
    del df['salary.salaries.val.basePayCount']
    del df['salary.salaries.val.salaryType']
    df.to_csv('../raw_data/formatted_UK_salary_salaries.csv')

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

def merge(df1, df2):
    return

def delete_dups():
    salary_fieldnames = ['gaTrackerData.jobId', 'jobTitle', 'payPeriod', 'payPercentile50', 'payPercentile10', 'payPercentile90']
    highlight_fieldnames = ['gaTrackerData.jobId', 'icon', 'name', 'highlightPhrase']

    # delete dup highlights
    check_df = pd.read_csv('glassdoor_usuk_edit_geo.csv')
    us_df = pd.read_csv('../raw_data/formated_US_highlights.csv')
    df = pd.read_csv('../raw_data/formatted_UK_benefits_highlights.csv')
    cond = df['gaTrackerData.jobId'].isin(check_df['gaTrackerData.jobId']) == False
    df.drop(df[cond].index, inplace=True)
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    df.to_csv('../raw_data/formatted_usuk_highlights.csv', index=False)

    #delete dup salaries
    check_df = pd.read_csv('glassdoor_usuk_edit_geo.csv')
    df = pd.read_csv('../raw_data/formatted_UK_salary_salaries.csv')
    cond = df['gaTrackerData.jobId'].isin(check_df['gaTrackerData.jobId']) == False
    df.drop(df[cond].index, inplace=True)
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    df.to_csv('../raw_data/formatted_usuk_salaries.csv', index=False)


if __name__=="__main__":
    #execute(False)
    #execute(True)
    #filter_highlights_columns()
    #filter_salary_columns()
    delete_dups()
