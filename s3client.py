# -*- coding: utf-8 -*-

'''
Simple python script for connecting to 3s object storage,
creating buckets, uploading/downloading/deleting files.
'''
import boto
import boto.s3
import sys
import os
import boto.s3.connection
import json
from boto.s3.key import Key

# Got from http://docs.ceph.com/docs/master/install/install-ceph-gateway
def s3connect( config_file ):
    "Connect to given s3 gateway using config file."
    
    try:
        with open( config_file ) as cfg_file:    
            conn_data = json.load(cfg_file)
    except:
        print("Error: Unable to read config file.")
        sys.exit(1)

    s3gw = conn_data['gateway']   
    access_key = conn_data['access_key']
    secret_key = conn_data['secret_key']
    port = conn_data['port']
    global conn
    conn = boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host=s3gw, port=port,                                                          
        is_secure=False, calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
    return conn; 

def buck_list():
    "Get avaliable buckets."
    
    print("Available buckets are:")
    for bucket in conn.get_all_buckets():
        print("{name} {created}".format(
            name=bucket.name,
            created=bucket.creation_date,
        )
        )
def buck_add( buck_name ):
    "Create bucket."
    
    buck = conn.create_bucket( buck_name )
    return buck;

#Bucket delete function to be here.
    
# Got from https://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto
def put_file( buck_name, file_name ):
    "Insert file to bucket. Create bucket if not exists."
    
    buck = conn.create_bucket( buck_name )
    print('Uploading %s to bucket %s' % \
    (file_name, buck)
    ) 
    def percent_cb(complete, total):
        "Internal 'progress bar' function. Move it higher?"
        
        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(buck)
    k.key =  os.path.basename(file_name)
    k.set_contents_from_filename(file_name,
        cb=percent_cb, num_cb=10)

def put_dir( buck_name, dir_name ):
    buck = conn.get_bucket( buck_name )
    # list of files in bucket
    skiped = 0
    uploaded = 0
    in_buck = []
    for key in buck.list():
        in_buck.append(key.name)

    for root, dirs, files in os.walk( dir_name ):
        for filename in files:
            # construct the full local path
            local_path = os.path.join(root, filename)
            if  filename in in_buck:
                # print 'File "%s" already in "%s"' % (filename, buck_name)
                skiped = skiped + 1
            else:
                put_file( buck_name, local_path )
                uploaded = uploaded + 1                
    print("New files uploaded:   " + str(uploaded))
    print("Existed files skiped: " + str(skiped))
    

def del_file( buck_name, file_name ):
    "Delete file from bucket."
    
    buck = conn.get_bucket( buck_name )
    print('Deleting %s from bucket %s' % \
    (file_name, buck)
    )
    buck.delete_key(file_name)
        
# Got from http://docs.ceph.com/docs/master/radosgw/s3/python/
def buck_cont( buck_name ):
    "View bucket contents."
    
    buck = conn.get_bucket( buck_name )
    for key in buck.list():
        print("{name}\t{size}\t{modified}".format(
            name = key.name,
            size = key.size,
            modified = key.last_modified,
        )
        )

def buck_dump_all( buck_name, dump_path ):
    "Retreive bucket  contents and  store it as  files."
    
    buck = conn.get_bucket( buck_name )
    for key in buck.list():
        buck.get_key( 'key' )
        key.get_contents_to_filename( dump_path  + key.name )

def buck_dump_diff( buck_name, dump_path ):
    "Dump new buckets only, skip existing."

    buck = conn.get_bucket( buck_name )
    dumped = 0
    skiped = 0
    errors = 0
    for key in buck.list():
        if os.path.isfile( dump_path + key.name):
            skiped = skiped + 1
            # print "Object " + key.name + " already exists in " + dump_path
        else:
            try:
                key.get_contents_to_filename( dump_path  + key.name )
                dumped = dumped + 1
                # print "Dumped " + key.name + " to " +  dump_path
            except:
                # print "Error dumping " + key.name + " to " +  dump_path
                errors = errors + 1
    print("New files dumped:     " + str(dumped))
    print("Existed files skiped: " + str(skiped))    
    print("Errors:               " + str(errors)) 

# Got from http://boto.cloudhackers.com/en/latest/s3_tut.html
def set_rights( buck_name , file_name):
    "Set read rights on file to public."
    
    buck = conn.get_bucket(buck_name)
    #acl = bucket.get_acl()
    #bucket.set_acl('public-read')
    buck.set_acl('public-read', file_name)    
    
if __name__ == '__main__':
    pass