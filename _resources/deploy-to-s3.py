import boto
import os
from boto.s3.key import Key


def deploy_to_S3(bucket, directory):
    deployed_files = []
    for path, d, files in os.walk(directory):
        for file in files:
            s3_filename = os.path.relpath(os.path.join(path, file), directory)
            local_path = os.path.join(path, file)
            k = Key(bucket)
            k.key = s3_filename
            print 'Uploading file %s' % local_path
            deployed_files.append(local_path)
            k.set_contents_from_filename(local_path)
    return deployed_files

conn = boto.connect_s3()
folder = '_site'
deployed_files = deploy_to_S3(conn.get_bucket('finyrdesign'), folder)
invalidation_list = [item.replace(folder, '') for item in deployed_files]
print 'Invalidating cloudfront distribution with {files}'.format(files=invalidation_list)
cf = boto.connect_cloudfront()
print cf.create_invalidation_request(os.environ["AWS_CLOUDFRONT_ID"], invalidation_list)
