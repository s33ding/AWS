# %%
import boto3
import pandas as pd
import json

with open ('/run/media/roberto/black-box/.syek/aws/s33ding.json', "r") as f:
    cred = json.load(f)

s3 = boto3.client('s3', region_name='us-east-1',aws_access_key_id=cred.get("id"), aws_secret_access_key=cred.get("secret"))

#%%
s3.create_bucket(Bucket= "trash-456")
#%%
s3.delete_bucket(Bucket="trash-456")
#%%

def printing_buckets():
    lst = []
    for bucket in  s3.list_buckets()['Buckets']:
        lst.append(bucket['Name'])
    print(f"My buckets: {lst}")

def search_bucket(bucket_nm):
    for bucket in s3.list_buckets()['Buckets']:
        if bucket_nm in bucket['Name']: 
          return bucket


# %%
fileSrc = './filesToUpload/mascot.jpeg'
keyName = 'linux.jpeg'
bucketName = 'roberto-server'

#uploading the files
s3.upload_file(Bucket = bucketName, Filename= fileSrc, Key = keyName)

#download the files
s3.download_file(Filename= keyName, Bucket= bucketName, Key = keyName)

#deleting object_key
s3.delete_object( Bucket=bucketName, Key=keyName)

# %%
# uploading the file with extra arg so that it can be public, for default aws files are upload as private for security reasons
s3.upload_file(
    Bucket = bucketName,
    Filename= fileSrc,
    Key = keyName, 
    ExtraArgs = {'ACL':'public-read'}
    )

# you can also make the entire bucket public with command bellow
s3.put_object_acl(Bucket= bucketName, Key = keyName, ACL = 'public-read')

url = 'https://{}.s3.amazonaws.com/{}'.format(bucketName, keyName); print(url)

# %%
htmlFileName = 'home.html'
fileSrcHtml = './filesToUpload/'+ htmlFileName

# Upload the lines.html file to S3
s3.upload_file(Filename=fileSrcHtml, 
               # Set the bucket name
               Bucket=bucketName, Key=htmlFileName,
               # Configure uploaded file
               ExtraArgs = {
                 # Set proper content type
                 'ContentType':'text/html',
                 # Set proper ACL
                 'ACL': 'public-read'})

# Print the S3 Public Object URL for the new file.
print("http://{}.s3.amazonaws.com/{}".format(bucketName, htmlFileName))

# %%

csvFile = './filesToUpload/campeonato-brasileiro-full.csv'
df = pd.read_csv(csvFile)

# upload a csv file as html
htmlFileName = 'campeonato-brasileiro-full.html'
fileSrcHtml = './filesToUpload/'+htmlFileName
df.to_html(fileSrcHtml, border=0, render_links=True)


# Upload the generated HTML to the gid-reports bucket
s3.upload_file(Filename= fileSrcHtml, Key=htmlFileName, Bucket=bucketName,
 ExtraArgs = {'ContentType': 'text/html', 'ACL': 'public-read'})

print("http://{}.s3.amazonaws.com/{}".format(bucketName, htmlFileName))
