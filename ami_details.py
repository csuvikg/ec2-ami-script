from typing import Optional


class AMIDetails:
    image_description: Optional[str]
    image_name: Optional[str]
    image_location: Optional[str]
    owner_id: Optional[str]
    instance_ids: list[str]

    def __init__(
        self,
        image_description: Optional[str] = None,
        image_name: Optional[str] = None,
        image_location: Optional[str] = None,
        owner_id: Optional[str] = None,
        instance_ids: list[str] = [],
    ) -> None:
        self.image_description = image_description
        self.image_name = image_name
        self.image_location = image_location
        self.owner_id = owner_id
        self.instance_ids = instance_ids

    def to_dict(self):
        return {
            "ImageDescription": self.image_description,
            "ImageName": self.image_name,
            "ImageLocation": self.image_location,
            "OwnerId": self.owner_id,
            "InstanceIds": self.instance_ids,
        }
