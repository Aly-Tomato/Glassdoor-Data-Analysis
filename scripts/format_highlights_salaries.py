"""
extract benefits.highlights into it's own CSV file
output headers = 'gaTrackerData.jobId', 'benefits.highlights'
"""
import pandas as pd
import csv
import ast

def main():
    og_csv = pd.read_csv('../raw_data/og_US_glassdoor.csv')
    #drop all completely empty rows from dataframe
    og_csv.dropna()

    # create new csv with only jobid & salaries column
    keep_col = ['gaTrackerData.jobId', 'salary.salaries']
    salaries_csv = og_csv[keep_col]
    #salaries_csv.drop(salaries_csv.columns[0], axis=1, inplace=True)
    salaries_csv.to_csv('US_salaries.csv', index=False)

    """
    # create new csv with only jobid & highlights columns
    keep_col = ['gaTrackerData.jobId', 'benefits.highlights']
    highlights_csv = og_csv[keep_col]
    highlights_csv.to_csv('US_highlights.csv', index=False)


    # create new US_glassdoor.csv with added ISO / currencyCode columns
    tot_rows, cols = og_csv.shape
    og_csv['salary.country.cc3LetterISO'] = ['USA' for i in range(0, tot_rows)]
    og_csv['salary.country.currencyCode'] = ['USD' for i in range(0, tot_rows)]

    columns = [m.strip('\n') for m in open('custom_fields.txt').readlines()]
    updated_csv = og_csv[columns]
    updated_csv.to_csv('updated_US_glassdoor.csv')
    """

def format_highlights():
    """
    Structures highlights csv to the following for each job highlight:
    jobId, icon, name, highlightphrase
    :return:
    """
    fieldnames = ['gaTrackerData.jobId', 'icon', 'name', 'highlightPhrase']

    with open('US_highlights.csv', 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('formated_US_highlights.csv', 'w+', newline='', encoding='UTF-8') as write_file:
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)
            writer.writeheader()

            for read_row in reader:
                try:
                    literals = ast.literal_eval(read_row['benefits.highlights'])
                except:
                    # continues if benefits.highlights is null
                    continue
                for literal in literals:
                    literal['gaTrackerData.jobId'] = read_row['gaTrackerData.jobId']
                    del literal['commentCount']
                    writer.writerow(literal)

def format_salaries():
    """
    :return:
    """
    fieldnames = ['gaTrackerData.jobId', 'jobTitle', 'payPeriod', 'payPercentile50', 'payPercentile10', 'payPercentile90']

    with open('US_salaries.csv', 'r', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('formated_US_salaries.csv', 'w+', newline='', encoding='UTF-8') as write_file:
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)
            writer.writeheader()

            for read_row in reader:
                try:
                    literals = ast.literal_eval(read_row['salary.salaries'])
                except:
                    # continues if benefits.highlights is null
                    continue
                for literal in literals:
                    literal['gaTrackerData.jobId'] = read_row['gaTrackerData.jobId']
                    spMap = literal.get('salaryPercentileMap')

                    if spMap:
                        literal['payPercentile50'] = spMap.get('payPercentile50')
                        literal['payPercentile90'] = spMap.get('payPercentile90')
                        literal['payPercentile10'] = spMap.get('payPercentile10')
                        del literal['salaryPercentileMap']
                    else:
                        literal['payPercentile50'] = None
                        literal['payPercentile90'] = None
                        literal['payPercentile10'] = None

                    del literal['basePayCount']
                    del literal['salaryType']
                    writer.writerow(literal)



if __name__ == '__main__':
    main()
    #format_highlights()
    format_salaries()

