from common.generators import generate_charset
from common.models import get_subclasses
from . import models
from .validators import ValidatorChain


def _check_slug(slug, classes) -> bool:
    return any([x.objects.filter(slug=slug).exists() for x in classes])


def check_block(sender, instance, **kwargs):
    validators = ValidatorChain(instance.validators)
    validators.check(instance)


def create_block(sender, instance, created, **kwargs):
    if created:
        slug = generate_charset(10)
        classes = get_subclasses(models.Block)
        while _check_slug(slug, classes):
            slug = generate_charset(10)

        instance.slug = slug
        instance.save(update_fields=["slug"])
