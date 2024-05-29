import json
import re
import boto3
from botocore.exceptions import ClientError

region_name = "eu-west-1"

session = boto3.Session(region_name=region_name)


def list_ami_usage(region_name: str) -> dict[str, list[str]]:
    ec2 = session.resource("ec2")

    result = dict()
    for instance in ec2.instances.all():
        image_id = instance.image_id
        result.setdefault(image_id, [])
        result[image_id].append(instance.instance_id)

    return result


def add_ami_details(ami_usage: dict[str, list[str]]) -> dict[dict, object]:
    ec2_client = session.client("ec2")

    all_amis = ami_usage.keys()
    invalid_amis = set()

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

    image_detail_results = dict()
    for image_detail in ami_details.get("Images", []):
        image_detail_results[image_detail["ImageId"]] = {
            "ImageDescription": image_detail.get("Description", None),
            "ImageName": image_detail.get("Name", None),
            "ImageLocation": image_detail.get("ImageLocation", None),
            "OwnerId": image_detail.get("OwnerId", None),
            "InstanceIds": ami_usage[image_detail["ImageId"]],
        }

    for ami in invalid_amis:
        image_detail_results[ami] = {
            "ImageDescription": None,
            "ImageName": None,
            "ImageLocation": None,
            "OwnerId": None,
            "InstanceIds": ami_usage[ami],
        }

    return image_detail_results


result = add_ami_details(list_ami_usage(region_name))

print(json.dumps(result, indent=4))
