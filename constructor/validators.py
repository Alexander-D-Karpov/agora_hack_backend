from constructor.services.validate_block import BaseValidator
from rest_framework.serializers import ValidationError


class ParentValidator(BaseValidator):
    def validate(self, block):
        if block.parent and block.parent.__class__.__name__ in ["Text", "Image", "Slider", "Iframe"]:
            raise ValidationError("You cant set this block as a parent")
