#Add given roles/policies to a given user

import boto3
from botocore.exceptions import ClientError

# Connect to IAM Service
IAM_CLIENT = boto3.client( 'iam' )

# Variables
username = input("USERNAME: ")
policy_arn = 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess' 


# Attach policy to a user
try:
    response = IAM_CLIENT.attach_user_policy(UserName = username, PolicyArn = policy_arn )
    print("Policy Attached...",  response)
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity':
        print( "User Not Found " )
    else:
        print( "Unexpected error:", e )

