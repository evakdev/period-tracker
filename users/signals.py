from users.models import User
from tracking.models import Trackable, Flow
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender = User)
def create_default_user_flow(sender, instance, created, **kwargs):
    if not created:
        return
    Flow.objects.create(user_id=instance.id)
    

@receiver(post_save, sender = Flow)
def create_flow_trackables(sender, instance, created, **kwargs):
    if not created:
        return
    user_id = instance.user_id
    trackables = [
        Trackable(name="Spotting", related_flow_id=instance.id, user_id=user_id),
        Trackable(name="Low", related_flow_id=instance.id, user_id=user_id),
        Trackable(name="Medium", related_flow_id=instance.id, user_id=user_id),
        Trackable(name="Heavy", related_flow_id=instance.id, user_id=user_id),
        Trackable(name="Very Heavy", related_flow_id=instance.id, user_id=user_id),
    ]
    Trackable.objects.bulk_create(trackables)
