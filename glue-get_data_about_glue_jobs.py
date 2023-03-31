import boto3
import pandas as pd
import os
import json


with open(os.environ['AWS_KEY'], "r") as f:
    credentials = json.load(f)

# Create a Boto3 session using the loaded credentials
session = boto3.Session(
    aws_access_key_id=credentials['id'],
    aws_secret_access_key=credentials['secret'],
    aws_session_token=credentials['token'],
    region_name='us-east-1'
)

def get_glue_job_names():
    """
    Get a list of Glue job names from the Glue service.
    
    Returns:
        A list of strings representing the Glue job names.
    """
    glue = session.client('glue')
    response = glue.get_jobs()
    job_names = [job['Name'] for job in response['Jobs']]
    return job_names

def get_last_job_run_info(glue_job_name):
    """
    Get the information about the last job run for a specified Glue job.
    
    Args:
        glue_job_name: A string representing the name of the Glue job.
    
    Returns:
        A dictionary containing the job name, job run ID, started on, and completed on (if available)
        for the last job run of the specified Glue job.
    """
    glue = session.client('glue')
    response = glue.get_job_runs(JobName=glue_job_name)
    job_runs = sorted(response['JobRuns'], key=lambda x: x['StartedOn'], reverse=True)

    last_job_run = job_runs[0]
    job_run_id = last_job_run['JobRunId']
    started_on = last_job_run['StartedOn'].isoformat()
    completed_on = last_job_run['CompletedOn'].isoformat() if 'CompletedOn' in last_job_run else None

    job_run_info = {'job_name': glue_job_name, 'job_run_id': job_run_id, 'started_on': started_on, 'completed_on': completed_on}
    return job_run_info

def get_last_job_runs_info_df():
    """
    Get a pandas DataFrame containing the job name, job run ID, started on, and completed on (if available)
    for the last job run of each Glue job.
    
    Returns:
        A pandas DataFrame containing the job run information for each Glue job.
    """
    job_names = get_glue_job_names()
    job_runs_info = [get_last_job_run_info(job_name) for job_name in job_names]
    job_runs_df = pd.DataFrame(job_runs_info, columns=['job_name', 'job_run_id', 'started_on', 'completed_on'])
    return job_runs_df

if __name__ == '__main__':
    job_runs_df = get_last_job_runs_info_df()
    job_runs_df.to_parquet("job_runs_df.parquet")
    print(job_runs_df)
