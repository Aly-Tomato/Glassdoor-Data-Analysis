import requests
import yaml
import logging
import json
import csv

logging.getLogger().setLevel(logging.INFO)


with open('config.yml') as config_file:
    config = yaml.safe_load(config_file)


def load_unique_job_ids():
    return [m.strip('\n') for m in open('US_unique_jobids.txt').readlines()]


def get_job_info(job_id):
    url = 'https://www.glassdoor.com/Job/json/details.htm?jobListingId={job_id}'.format(job_id=job_id)
    try:
        json_data = requests.get(url, headers=config['headers']).json()
        return json_data
    except json.decoder.JSONDecodeError:
        print('ERROR FOUND: retrying request ' + job_id)


def write_json(data, idx):
    with open('results/file_{}.json'.format(idx), 'w', encoding='UTF-8') as json_file:
        for result in data:
            json_file.write(json.dumps(result, ensure_ascii=False))
            json_file.write('\n')
    logging.info('file {} written'.format(idx))


def worker(job_id, columns, writer):
    json_data = get_job_info(job_id)
    job = {}

    for c in columns:
        try:
            job[c] = get_field_data(json_data, c)
        except:
            job[c] = None
    try:
        writer.writerow(job)
    except:
        print(job_id, json)

def get_field_data(json, field):
    objects = field.split('.')
    for o in objects:
        json = json.get(o)
    return json

def divide_chunks(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def execute():
    data = load_unique_job_ids()
    chunks = divide_chunks(data, 400)

    #create csv with header
    columns = [m.strip('\n') for m in open('custom_fields.txt').readlines()]
    with open('US_glassdoor.csv', 'a+', newline='', encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for idx, chunk in enumerate(chunks):
            for job_id in chunk:
                worker(job_id, columns, writer)

            #write_json(row, idx)


if __name__ == '__main__':
    execute()
