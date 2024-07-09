from django.db import models

from user.models import Patient, VisitTime, Doctor


class Reservation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_time = models.ForeignKey(VisitTime, on_delete=models.CASCADE)


class Transaction(models.Model):
    from_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    to_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)