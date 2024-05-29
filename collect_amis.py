import boto3

region_name = "eu-west-1"


def list_amis(region_name: str) -> list[str]:
    session = boto3.Session(region_name=region_name)
    ec2 = session.resource("ec2")

    instances = ec2.instances.all()
    ami_ids = {instance.image_id for instance in instances}

    return list(ami_ids)


for ami in list_amis(region_name):
    print(ami)
