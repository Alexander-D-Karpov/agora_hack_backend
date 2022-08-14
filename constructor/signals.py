from django.db.models.signals import post_save
from django.dispatch import receiver

from common.generators import generate_charset
from constructor.models.base import Block


@receiver(post_save, sender=Block)
def create_player(sender, instance, created, **kwargs):
    if created:
        instance.slug = generate_charset(10)
        instance.save(update_fields=["slug"])
