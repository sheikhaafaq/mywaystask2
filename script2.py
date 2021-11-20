#list of imported Modules/Library
#Make a user with specific roles and policies
import boto3
from botocore.exceptions import ClientError
import json

# Connect to IAM Service
IAM_CLIENT = boto3.client( 'iam' )

# Variables
username = input("USERNAME: ")
policy_arn = 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess' 
tags=[ # adding tags to identify that user in IAM
        {
            'Key': 'Env',
            'Value': 'Test'
        }
    ]

policy_name = "MyAmazonS3ReadOnlyAccess" #input("POLICY NAME: ")
#AmazonS3ReadOnlyAccess
policy_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "*"
        }
    ]
}
#--------------------------------------------------------------------------------------
# Create User
try:
    user = IAM_CLIENT.create_user(UserName = username, Tags = tags)
    print("User Created... ", user)
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print( "User already exists" )
    else:
        print( "Unexpected error:", e )

# Create Policy
try:
    policy_res = IAM_CLIENT.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_json)
    )

   # Attach policy to a user
    response = IAM_CLIENT.attach_user_policy(
    UserName = username, 
    PolicyArn = policy_res['Policy']['Arn'] )
    print("Policy Attached...")
except ClientError as error:
    if error.response['Error']['Code'] == 'EntityAlreadyExists':
        print('Policy already exists... hence using the same policy')  
    else:
        print('Unexpected error occurred...', error)





