import boto3

# --- Configuration Variables ---
# The region where the VM will be launched
REGION = 'us-east-1' 
# The ID of the OS image (Amazon Machine Image - AMI) 
# Example: a standard Amazon Linux 2 AMI
AMI_ID = 'ami-0abcdef1234567890' 
# The size of the VM (e.g., t2.micro is the smallest free-tier eligible)
INSTANCE_TYPE = 't2.micro'
# The key pair name used for SSH access. You must have this key already created in AWS.
KEY_PAIR_NAME = 'My-EC2-Key' 
# The Security Group ID (Firewall rules). You should have a pre-configured group.
SECURITY_GROUP_ID = 'sg-0123456789abcdef0' 
# Tag Name for the instance
INSTANCE_NAME = 'My-New-Python-VM'
# --- End Configuration Variables ---

def create_ec2_instance():
    """
    Launches a new EC2 instance (Virtual Machine) in AWS.
    """
    print(f"Connecting to EC2 in region: {REGION}...")
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2', region_name=REGION)

    try:
        # Call the run_instances API to launch the VM
        response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            KeyName=KEY_PAIR_NAME,
            SecurityGroupIds=[SECURITY_GROUP_ID],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': INSTANCE_NAME
                        },
                    ]
                },
            ]
        )

        # Retrieve the ID of the new instance
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Successfully launched new EC2 Instance! 🚀")
        print(f"Instance ID: {instance_id}")
        
        return instance_id

    except Exception as e:
        print(f"An error occurred during VM creation: {e}")
        return None

if __name__ == '__main__':
    create_ec2_instance()
