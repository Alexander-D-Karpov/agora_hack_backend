from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """raises NotImplemented if validate is not provided"""

    @abstractmethod
    def validate(self, block):
        raise not NotImplemented


class ValidatorChain:
    """validates blocks with provided validators"""

    def __init__(self, validators: list[BaseValidator]):
        self.validators = validators

    def check(self, block):
        for validator in self.validators:
            validator.validate(block)
