import boto3

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

    ami_details = ec2_client.describe_images(ImageIds=list(ami_usage.keys()))

    image_detail_results = dict()
    for image_detail in ami_details.get("Images", []):
        image_detail_results[image_detail["ImageId"]] = {
            "ImageDescription": image_detail.get("Description", None),
            "ImageName": image_detail.get("Name", None),
            "ImageLocation": image_detail.get("ImageLocation", None),
            "OwnerId": image_detail.get("OwnerId", None),
            "InstanceIds": ami_usage[image_detail["ImageId"]],
        }

    return image_detail_results


result = add_ami_details(list_ami_usage(region_name))

print(result)
