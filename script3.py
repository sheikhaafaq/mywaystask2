# Make new roles/policies with specific access
import json, boto3
from botocore.exceptions import ClientError

#--------------------------->> CREATE OBJECT OF IAM RESOURCE <<-------------------------

iam_client = boto3.client('iam')

#--------------------------->> CREATE IAM ROLE <<---------------------------------------

def createIamRole(role_name, trust_relationship_policy_another_aws_service ):
    try:
        create_role_res = iam_client.create_role(
            RoleName= role_name,
            AssumeRolePolicyDocument=json.dumps(trust_relationship_policy_another_aws_service),
            Description='This is a test role',
            Tags=[
                {
                    'Key': 'Owner',
                    'Value': 'msb'
                }
            ]
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            return 'Role already exists...'
        else:
            return 'Unexpected error occurred... Role could not be created', error 
    return create_role_res



#-------------------------->> CREATE IAM POLICY <<-----------------------------------


def createIamPolicy(policy_name,role_name):
    try:
        policy_res = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            return 'Policy already exists... hence using the same policy'   
        else:
            print('Unexpected error occurred... hence cleaning up', error)
            iam_client.delete_role(
                RoleName= role_name
            )
            return 'Role could not be created...', error
    return policy_res


#-----------------------------ATTACH POLICY TO ROLE------------------------------

def attachPolicyToRole(role_name, policy_arn):
    try:
        policy_attach_res = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    except ClientError as error:
        print('Unexpected error occurred... hence cleaning up')
        iam_client.delete_role(
            RoleName= role_name
        )
        return 'Role could not be created...', error
    return policy_attach_res


#---------------------->> DEFINE VARIABLES <<-----------------------------------

trust_relationship_policy_another_aws_service = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

policy_json = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "ec2:*"
        ],
        "Resource": "*"
    }]
}

roleName = input('ROLE_NAME: ')
policyName = input('POLICY_NAME: ')


#------------------------->> INVOKE FUNCTIONS <<---------------------------------
IamRoleRes = createIamRole(roleName, trust_relationship_policy_another_aws_service)
print(IamRoleRes)

IamPolicyRes = createIamPolicy(policyName, roleName)
print(IamPolicyRes)

attachPolicyRes = attachPolicyToRole(roleName, IamPolicyRes['Policy']['Arn'])
print(attachPolicyRes)



