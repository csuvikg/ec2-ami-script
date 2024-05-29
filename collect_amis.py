import boto3

region_name = "eu-west-1"

session = boto3.Session(region_name=region_name)


def list_amis(region_name: str) -> list[str]:
    ec2 = session.resource("ec2")

    instances = ec2.instances.all()
    ami_ids = {instance.image_id for instance in instances}

    return list(ami_ids)


def describe_amis(ami_ids: list[str]) -> dict[dict, object]:
    ec2_client = session.client("ec2")

    ami_details = ec2_client.describe_images(ImageIds=ami_ids)

    image_detail_results = dict()
    for image_detail in ami_details.get("Images", []):
        image_detail_results[image_detail["ImageId"]] = {
            "ImageDescription": image_detail.get("Description", None),
            "ImageName": image_detail.get("Name", None),
            "ImageLocation": image_detail.get("ImageLocation", None),
            "OwnerId": image_detail.get("OwnerId", None),
            "InstanceIds": [],
        }

    return image_detail_results


result = describe_amis(list_amis(region_name))

print(result)