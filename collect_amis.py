import json
import re
import boto3
from botocore.exceptions import ClientError

from ami_details import AMIDetails

AMIUsageDict = dict[str, list[str]]

region_name = "eu-west-1"

session = boto3.Session(region_name=region_name)


def list_ami_usage(region_name: str) -> AMIUsageDict:
    ec2 = session.resource("ec2")

    result: AMIUsageDict = dict()
    for instance in ec2.instances.all():
        image_id = instance.image_id
        result.setdefault(image_id, [])
        result[image_id].append(instance.instance_id)

    return result


def add_ami_details(ami_usage: AMIUsageDict) -> dict[str, AMIDetails]:
    ec2_client = session.client("ec2")

    all_amis = ami_usage.keys()
    invalid_amis: set[str] = set()

    is_finished = False
    while not is_finished:
        try:
            ami_details = ec2_client.describe_images(
                ImageIds=list(all_amis - invalid_amis)
            )
            is_finished = True
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAMIID.NotFound":
                error_message = e.response["Error"]["Message"]
                found_amis = re.findall(r"ami-\w+", error_message)
                invalid_amis.update(found_amis)

    ami_details_result = dict()
    for image_detail in ami_details.get("Images", []):
        ami_details_result[image_detail["ImageId"]] = AMIDetails(
            image_detail.get("Description", None),
            image_detail.get("Name", None),
            image_detail.get("ImageLocation", None),
            image_detail.get("OwnerId", None),
            ami_usage[image_detail["ImageId"]],
        )

    for ami in invalid_amis:
        ami_details_result[ami] = AMIDetails(instance_ids=ami_usage[ami])

    return ami_details_result


result = add_ami_details(list_ami_usage(region_name))
serializable_result = {k: v.to_dict() for k, v in result.items()}

print(json.dumps(serializable_result, indent=4))
