from django.db.models.signals import pre_save, post_save
from .models import Event
from ..users.models import Notification
from django.dispatch import receiver


@receiver(post_save, sender=Event)
def notification_to_subscribers(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        text = f'В вашем городе произойдет мероприятие! {instance.title}'
        notification = Notification.objects.create(user=user, content=text)
        notification.save()
