from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from server.apps.deals.models import Deal


@receiver(post_save, sender=Deal)
def clear_cache(sender, **kwargs):
    """ Чистит кэш, если был сохранён объект Deal. """

    cache.clear()
