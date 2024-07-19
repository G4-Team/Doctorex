from django.db import models

from user.models import Account, Doctor, Patient, VisitTime


class Reservation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_time = models.ForeignKey(VisitTime, on_delete=models.CASCADE)


class Transaction(models.Model):
    from_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    to_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class Comment(models.Model):
    scores = {
        1: "خیلی بد",
        2: "بد",
        3: "متوسط",
        4: "خوب",
        5: "خیلی خوب",
    }
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="comments"
    )
    score = models.IntegerField(choices=scores, default=3)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="comments"
    )
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
