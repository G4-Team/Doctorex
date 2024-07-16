from django.db import connection, reset_queries, transaction
from django.db.models import F
from django.db.models.signals import ModelSignal, post_delete, post_save
from django.dispatch import receiver

from .models import Comment


@receiver(signal=post_save, sender=Comment)
def update_avg_rate_when_new_comment(
    sender: ModelSignal,
    instance: Comment,
    created: bool,
    **kwargs,
):
    reset_queries()
    if created:
        with transaction.atomic():
            count = Comment.objects.filter(doctor__id=instance.doctor.pk).count()
            instance.doctor.avg_rate = (
                F("avg_rate") * (count - 1) + instance.score
            ) / (count)
            instance.doctor.save()
    for q in connection.queries:
        print(q)


@receiver(signal=post_delete, sender=Comment)
def update_avg_rate_when_delete_comment(
    sender: ModelSignal,
    instance: Comment,
    **kwargs,
):
    reset_queries()
    with transaction.atomic():
        count = Comment.objects.filter(doctor__id=instance.doctor.pk).count()
        if count == 0:
            instance.doctor.avg_rate = 0
        else:
            instance.doctor.avg_rate = (
                F("avg_rate") * (count + 1) - instance.score
            ) / (count)
        instance.doctor.save()
    for q in connection.queries:
        print(q)
