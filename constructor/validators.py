from rest_framework.serializers import ValidationError
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """raises NotImplemented if validate is not provided"""

    @abstractmethod
    def validate(self, block, **kwargs):
        raise not NotImplemented


class ValidatorChain:
    """validates blocks with provided validators"""

    def __init__(self, validators):
        self.validators = validators

    def check(self, block):
        for validator in self.validators:
            val = validator()
            val.validate(block)


class ParentValidator(BaseValidator):
    def validate(self, block, **kwargs):
        if block.parent and not block.parent.__class__.is_parent:
            raise ValidationError("You cant set this block as a parent")


class BaseCssValidator(BaseValidator):
    def _check_num(self, num) -> bool:
        try:
            float(num)
            return True
        except ValueError:
            pass
        return False

    def _check(self, val, name, extra_vals=None):
        if extra_vals is None:
            extra_vals = []
        if val in ["inherit", "initial", "unset", "auto", "none"] + extra_vals:
            return
        else:
            for el in ["px", "%", "em"]:
                if el in val:
                    num = val.split(el)[0].split()[0]
                    if self._check_num(num):
                        return
        raise ValidationError(f"field {name} is not css compatible")

    def validate(self, block, **kwargs):
        if "field" in kwargs:
            value = getattr(block, kwargs["field"])
            self._check(
                value,
                kwargs["field"],
                extra_vals=kwargs["extra_vals"] if "extra_vals" in kwargs else None,
            )
            return
        elif "fields" in kwargs:
            [
                self._check(
                    getattr(block, x),
                    x,
                    extra_vals=kwargs["extra_vals"] if "extra_vals" in kwargs else None,
                )
                for x in kwargs["fields"]
            ]
            return
        raise NotImplementedError


class MarginPaddingValidator(BaseCssValidator):
    def validate(self, block, **kwargs):
        super(MarginPaddingValidator, self).validate(
            block,
            fields=[
                "margin_right",
                "margin_left",
                "margin_bottom",
                "margin_top",
                "padding_right",
                "padding_left",
                "padding_bottom",
                "padding_top",
            ],
        )


class SizeValidator(BaseCssValidator):
    def validate(self, block, **kwargs):
        super(SizeValidator, self).validate(
            block,
            fields=[
                "width",
                "height",
            ],
            extra_vals=[
                "max-content",
                "min-content",
                "available",
                "fit-content",
                "border-box",
                "border-box",
                "fill",
            ],
        )
