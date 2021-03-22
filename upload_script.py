import boto3

#Uploading data files to the s3 bucket
s3 = boto3.resource('s3')
# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
# Upload the data files
data = open('filename', 'rb')
s3.Bucket('your bucket').put_object(Key='file name', Body=data)
return