class AMIDetails:
    image_description: str
    image_name: str
    image_location: str
    owner_id: str
    instance_ids: list[str]

    def __init__(
        self,
        image_description: str = None,
        image_name: str = None,
        image_location: str = None,
        owner_id: str = None,
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
