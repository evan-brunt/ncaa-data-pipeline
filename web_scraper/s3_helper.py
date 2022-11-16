import boto3
import os
import glob
from config_helper import config


def add_files_from_dir_to_s3(bucket_name, directory):
    key = config['AWS']['KEY']
    secret = config['AWS']['SECRET']
    s3 = boto3.resource('s3', region_name="us-east-1", aws_access_key_id=key, aws_secret_access_key=secret)
    bucket = s3.Bucket(bucket_name)
    for path in glob.iglob(directory + '**/*.json', recursive=True):
        s3_file_path = os.path.join(*path.split('/')[4:])
        bucket.upload_file(path, s3_file_path)


if __name__ == '__main__':
    add_files_from_dir_to_s3('ebrunt-espn-data', '/Users/ebrunt/Desktop/ncaa-data/')
