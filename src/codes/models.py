from django.db import models
from users.models import NewUser as nu
import random
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(nu, on_delete=models.CASCADE)
    codeentertimer = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)