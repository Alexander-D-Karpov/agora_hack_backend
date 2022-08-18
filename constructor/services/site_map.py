from django.shortcuts import get_object_or_404

from constructor.models import Site, Block


def get_site_map(slug: str) -> list:
    site = get_object_or_404(Site, name=slug)

    blocks = [x.get_json() for x in Block.objects.filter(parent__isnull=True, site=site)]

    return blocks
