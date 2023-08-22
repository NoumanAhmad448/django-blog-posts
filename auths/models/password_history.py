from django.db import models
import datetime

class PasswordHistory(models.Model):
    user_id = models.IntegerField(max_length=50)
    created_at = models.DateField(default=datetime.date.today())