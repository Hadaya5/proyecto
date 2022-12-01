import re
import boto3
from botocore.exceptions import ClientError
from PIL import Image
import os
with open('config/aws','r') as h:
    awscredentials = h.read().split()
def remove_oid(string):
    while True:
        pattern = re.compile('{\s*"\$oid":\s*(\"[a-z0-9]{1,}\")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string

def compressMe(file, filename):
    picture = Image.open(file)
    picture.thumbnail((500,500), Image.ANTIALIAS)
    picture.save("/tmp/"+filename,"JPEG",optimize = True,quality = 80)
    upload_file("/tmp/"+filename,filename)

def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id=awscredentials[0],aws_secret_access_key=awscredentials[1])
    try:
        response = s3_client.upload_file(file_name, 'atinet', 'images/' + object_name)
        print('images/' + object_name)
    except ClientError as e:
        print('error',e)
        return False
    return True